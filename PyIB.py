""" module to simplify data access from IB """
from threading import Thread
import queue
# import datetime as dt
# import time
from PyIbConsts import PyIbConsts
from ibapi.wrapper import EWrapper
from ibapi.client import EClient
from ibapi.common import BarData
from ibapi.contract import Contract


class MarketDataWrapper(EWrapper):
    """callback for ib market data"""
    def init_error(self):
        """ sets errors queue anew """
        error_queue=queue.Queue()
        self._my_errors = error_queue

    def get_error(self, timeout=PyIbConsts.IbTimeoutSec):
        ''' gets errors from wrapper '''
        if self.is_error():
            try:
                return self._my_errors.get(timeout=timeout)
            except queue.Empty:
                print("queue returned empty")
                return None

        return None

    def is_error(self):
        ''' has errors? '''
        return not self._my_errors.empty()

    def error(self, id, errorCode, errorString):
        ''' constructs error message and pushes it into _my_errors '''
        errormsg = "IB error id %d errorcode %d string %s" % (id, errorCode, errorString)
        self._my_errors.put(errormsg)

    def init_response_queue(self):
        ''' takes care of the threading '''
        response_queue=queue.Queue()
        self._response_queue = response_queue
        self.tickTypes = PyIbConsts.RequestedTickTypes # needed for getMktData

        return response_queue

    def historicalData(self, reqId:int, bar:BarData):
        if bar:
            print("HistoricalData. ", reqId, " Date:", bar.date, 
                    "Open:", bar.open, "High:", bar.high, "Low:", bar.low, "Close:", bar.close, 
                    "Volume:", bar.volume, "Count:", bar.barCount)
            self._response_queue.put(
                {"Date": bar.date, 
                 "Open": bar.open, "High": bar.high, "Low": bar.low, "Close": bar.close, 
                 "Volume": bar.volume})
        else:
            self._response_queue.put(0)

    def tickPrice(self, reqId, tickType, price, attrib):
        ''' Handle tickPrice event  - this is the callback function '''
        if tickType in self.tickTypes:
            self._response_queue.put({"tickType": tickType, "price": price})
            self.tickTypes.remove(tickType)

        if not self.tickTypes: # len(self.tickTypes) == 0:
            self._response_queue.put(0)
        

class MarketDataClient(EClient):
    ''' class for sending request to server '''
    def __init__(self, wrapper):
        ## Set up the callback-wrapper 
        EClient.__init__(self, wrapper)

    def get_historic_data(self, contract):
        ''' sends request for historic data '''
        duration = "1 D"
        barsize = "1 day"
        # endDatetime = (dt.datetime.today() - dt.timedelta(days=180)).strftime("%Y%m%d %H:%M:%S")
        enddate = "" # today 
        desiredinfo = "MIDPOINT" if contract.secType == "CASH" else "TRADE"
        onlyreghours = 1 # yes, only regular trade-hours   
        # NOTE: !!!!  Hofni, correct??? 

        formatdate = 1  # (yyyyMMdd) this format is mandatory for daily info 
        needrt = False  # need realtime: nope. (keepUpToDate)

        # define response queue (thread that polls for data and stores it)
        # 'polling' means to ask every once in a while if there's new info
        response_queue=self.wrapper.init_response_queue()

        ## The return value for this function.
        result = []

        reqid = 4101 # as listed in IB Samples. Could be that 1 is valid as well. 
        self.reqHistoricalData(reqid, contract, enddate, duration, barsize, desiredinfo, 
                                onlyreghours, formatdate, needrt, [])

        MAX_WAIT_SECONDS = PyIbConsts.IbTimeoutSec

        try:
            while True:
                response = response_queue.get(timeout=MAX_WAIT_SECONDS)
                if response == 0:
                    break

                result.append(response)
        except queue.Empty:
            print("Could not retrieve all data, timed out.")

        return result


    def get_market_data(self, contract):
        ''' sets up request for market data '''
        print("Asking market data for contract", contract)

        # define response queue (thread that polls for data and stores it)
        # 'polling' means to ask every once in a while if there's new info
        response_queue=self.wrapper.init_response_queue()

        ## The return value for this function.
        result = []

        myreqid = 1101
        self.reqMarketDataType( PyIbConsts.MarketdataTypeDELAYED ) # 3
        self.reqMktData(myreqid, contract, "", False, False, []) 

        MAX_WAIT_SECONDS = PyIbConsts.IbTimeoutSec

        try:
            while True:
                response = response_queue.get(timeout=MAX_WAIT_SECONDS)
                if response == 0:
                    break

                result.append(response)
        except queue.Empty:
            print("Could not retrieve all data, timed out.")

        return result

class IbApp(MarketDataWrapper, MarketDataClient):
    ''' class initiates request and sets up the response callback '''
    def __init__(self, ipaddress, portid, clientid):
        MarketDataWrapper.__init__(self)
        MarketDataClient.__init__(self, wrapper=self)

        self.connect(ipaddress, portid, clientid)
        self.init_error()

        thread = Thread(target = self.run)
        thread.start()

        setattr(self, "_thread", thread)