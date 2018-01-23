from ibapi.contract import Contract
# // https://github.com/quantrocket-llc/ibapi-grease

import PyIB
from PyIbConsts import PyIbConsts

class PyIbCaller:
    ''' class to import symbol from ib '''

    @staticmethod
    def GetHistoricData(symbol, securityType, currency, exchange, monthYYYYMM):
        app = PyIB.IbApp(PyIbConsts.IbIpAddress, PyIbConsts.IbPort, PyIbConsts.IbClientId)

        contract = Contract()
        contract.symbol = symbol         # "CL"  #      ESTX50" # "GBP"
        contract.secType =  securityType #"FUT" #   IND"    # "CASH"
        contract.currency = currency     # "USD" #   EUR"    # "USD"
        contract.exchange = exchange     # "NYMEX" # DTB"    # "IDEALPRO"
        if securityType == "FUT":
            contract.lastTradeDateOrContractMonth = monthYYYYMM  
        # see: contract definition here: 
        #   https://interactivebrokers.github.io/tws-api/classIBApi_1_1Contract.html
        # and here: https://interactivebrokers.github.io/tws-api/basic_contracts.html#gsc.tab=0

        # https://interactivebrokers.github.io/tws-api/tick_types.html#gsc.tab=0

        # data = app.get_market_data(contract)
        data = app.get_historic_data(contract)

        try:
            app.disconnect()
            
        except (KeyboardInterrupt, SystemExit):
            # see http://effbot.org/zone/stupid-exceptions-keyboardinterrupt.htm
            raise
        except:
            print("already disconnected")

        return data
