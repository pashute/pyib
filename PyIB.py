""" module docstring here """
from ibapi.wrapper import EWrapper
from ibapi.client import EClient
from ibapi.contract import *
from threading import Thread
import queue
import time
from IbConsts import IbConsts


class MarketDataWrapper(EWrapper):
    """callback for ib market data"""
    def init_error(self):
        """ sets errors queue anew """
        error_queue=queue.Queue()
        self._my_errors = error_queue

    def get_error(self, timeout=IbConsts.IbTimeoutSec):
        ''' gets errors from wrapper '''
        if self.is_error():
            try:
                return self._my_errors.get(timeout=timeout)
            except queue.Empty:
                print("queue returned empty")
                return None

        return None

    def is_error(self):
        """ is error? """
        an_error_if=not self._my_errors.empty()
        return an_error_if

    def error(self, id, errorCode, errorString):
        ''' the error itself '''
        errormsg = "IB error id %d errorcode %d string %s" % (id, errorCode, errorString)
        self._my_errors.put(errormsg)

    def init_response_queue(self, tickTypes):
        ''' take care of the threading '''
        response_queue=queue.Queue()
        self._response_queue = response_queue
        self.tickTypes = tickTypes

        return response_queue

    def tickPrice(self, reqId, tickType, price, attrib):
        ''' handle tickPrice event  '''
        if tickType in self.tickTypes:
            self._response_queue.put({"tickType": tickType, "price": price})
            self.tickTypes.remove(tickType)

        if len(self.tickTypes) == 0:
            self._response_queue.put(0)
        

class MarketDataClient(EClient):
    def __init__(self, wrapper):
        ## Set up with a wrapper inside
        EClient.__init__(self, wrapper)

    def get_market_data(self, contract, tickTypes):
        print("Asking market data for contract", contract)

        ## Make a place to store the tick data we are returning.
        ## This is a queue
        response_queue=self.wrapper.init_response_queue(tickTypes)

        ## The return value for this function.
        result = []

        myreqid = 1101
        self.reqMarketDataType( IbConsts.MarketdataTypeDELAYED ) # 3
        self.reqMktData(myreqid, contract, "", False, False, []) # 1101

        MAX_WAIT_SECONDS = IbConsts.IbTimeoutSec

        try:
            while True:
                response = response_queue.get(timeout=MAX_WAIT_SECONDS)
                if response == 0:
                    break

                result.append(response)
        except queue.Empty:
            print("Could not retrieve all data, timed out.")

        return result

class TestApp(MarketDataWrapper, MarketDataClient):
    def __init__(self, ipaddress, portid, clientid):
        MarketDataWrapper.__init__(self)
        MarketDataClient.__init__(self, wrapper=self)

        self.connect(ipaddress, portid, clientid)
        self.init_error()

        thread = Thread(target = self.run)
        thread.start()

        setattr(self, "_thread", thread)


if __name__ == '__main__':
    app = TestApp(IbConsts.IbIpAddress, IbConsts.IbPort, IbConsts.IbClientId)

    contract = Contract()
    contract.symbol = "CL" #      ESTX50" # "GBP"
    contract.secType =  "FUT" #   IND"    # "CASH"
    contract.currency = "USD" #   EUR"    # "USD"
    contract.exchange = "NYMEX" # DTB"    # "IDEALPRO"
    contract.lastTradeDateOrContractMonth = "201802" 
	# see: contract definition here: 
	#   https://interactivebrokers.github.io/tws-api/classIBApi_1_1Contract.html
	# and here: https://interactivebrokers.github.io/tws-api/basic_contracts.html#gsc.tab=0

    # https://interactivebrokers.github.io/tws-api/tick_types.html#gsc.tab=0

    data = app.get_market_data(contract, IbConsts.RequestedTickTypes)
    print(data)

    try:
        app.disconnect()
    except (KeyboardInterrupt, SystemExit):
		# see http://effbot.org/zone/stupid-exceptions-keyboardinterrupt.htm
        raise
    except:
        print("already disconnected")
	