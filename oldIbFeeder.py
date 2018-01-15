""" IB Feed module """
# https://qoppac.blogspot.co.il/2017/03/interactive-brokers-native-python-api.html
from ibapi.wrapper import EWrapper
from ibapi.client import EClient

import queue
from threading import Thread

from IbConsts import IbConsts as ibc


# from: 
class IbWrapper(EWrapper):
    """class to override callbacks from ib feed"""
    # error handling code

    def init_error(self):
        error_queue=queue.Queue()
        self._my_errors = error_queue

    def get_error(self, timeout=5):
        if self.is_error():
            try:
                return self._my_errors.get(timeout=timeout)
            except queue.Empty:
                return None

        return None

    def is_error(self):
        an_error_if=not self._my_errors.empty()
        return an_error_if

    def error(self, id, errorCode, errorString):
        ## Overriden method
        errormsg = "IB error id %d errorcode %d string %s" % (id, errorCode, errorString)
        self._my_errors.put(errormsg)

    # Time telling code
    def init_time(self):
        time_queue=queue.Queue()
        self._time_queue = time_queue

        return time_queue

    def current_time(self, time_from_server):
        # Overriden method
        self._time_queue.put(time_from_server)


class IbClient(EClient):
    def __init__(self, wrapper):
          EClient.__init__(self, wrapper)
    
    def telltime(self):
        wrptimer = self.wrapper.init_time()
        status = ""

        self.reqCurrentTime() # EClient request to server
        TIMEOUT_SECONDS = 10
        timedout = False

        try: 
            curtime = wrptimer.get(timeout=TIMEOUT_SECONDS)
        
        except queue.Empty:
            print("queue is empty")
            timedout = True
            curtime = None
        
            while self.wrapper.is_error():
                status = "{0}\n{1}".format(status, self.get_error())

        return curtime


class IbApp(IbWrapper, IbClient):
    def __init__(self, ipaddress, portid, clientid):
        IbWrapper.__init__(self)
        IbClient.__init__(self, wrapper=self)
        self.connect(ipaddress, portid, clientid)

        thread = Thread(target=self.run)
        thread.start()

        setattr(self, "_thread", thread) # x._thread = thread

        self.init_error()


if __name__ == '__main__':
    app = IbApp(ibc.IbIpAddress, ibc.IbPort, ibc.IbClientId)
    curtime = app.telltime()
    print(curtime)
    app.disconnect()