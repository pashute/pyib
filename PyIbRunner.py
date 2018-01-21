from ibapi.contract import Contract
// https://github.com/quantrocket-llc/ibapi-grease

import PyIB
from IbConsts import IbConsts

class PyIbRunner:
    ''' class to import symbol from ib '''

    @staticmethod
    def getMktData(symbol, securityType, currency, exchange, monthYYYYMM):
        app = PyIB.TestApp(IbConsts.IbIpAddress, IbConsts.IbPort, IbConsts.IbClientId)

        contract = Contract()
        contract.symbol = symbol # "CL"  #      ESTX50" # "GBP"
        contract.secType =  securityType #"FUT" #   IND"    # "CASH"
        contract.currency = currency     # "USD" #   EUR"    # "USD"
        contract.exchange = exchange     # "NYMEX" # DTB"    # "IDEALPRO"
        if securityType == "FUT":
            contract.lastTradeDateOrContractMonth = monthYYYYMM  
        # see: contract definition here: 
        #   https://interactivebrokers.github.io/tws-api/classIBApi_1_1Contract.html
        # and here: https://interactivebrokers.github.io/tws-api/basic_contracts.html#gsc.tab=0

        # https://interactivebrokers.github.io/tws-api/tick_types.html#gsc.tab=0

        data = app.get_market_data(contract, IbConsts.RequestedTickTypes)

        try:
            app.disconnect()
            
        except (KeyboardInterrupt, SystemExit):
            # see http://effbot.org/zone/stupid-exceptions-keyboardinterrupt.htm
            raise
        except:
            print("already disconnected")

        return data

if __name__ == '__main__':
    symbol       = "CL"  #      ESTX50" # "GBP"
    securityType = "FUT" #   IND"    # "CASH"
    currency     = "USD" #   EUR"    # "USD"
    exchange     = "NYMEX" # DTB"    # "IDEALPRO"
    monthYYYYMM  = "201802" 

    PyIbRunner.getMktData(symbol, securityType, currency, exchange, monthYYYYMM)

    