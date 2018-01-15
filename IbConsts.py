class IbConsts():
    ''' IB Feed consts '''

    IbIpAddress = '127.0.0.1'
    IbPort = 4001 # was 4002 for demo
    IbClientId = 999 # my choice    

    IbTimeoutSec = 15

    OrderTypeMKT = 'MKT'

    # https://www.interactivebrokers.com/en/index.php?f=products&p=fut
    SymbolTypeFUTURES = 'FUT'
    SymbolTypeETF = 'ETF'
    SymbolTypeINDEX = 'IND' 

    SymbolTypeSTOCK = 'STK'
    SymbolTypeFOREX = 'FX'
    SymbolTypeBOND = 'BOND'
    SymbolTypeCASH = 'CASH'



    ActionBUY = 'BUY'
    ActionSELL = 'SELL'

    ReqtypeBID = 'bid'
    ReqtypeASK = 'ask'

    IbExchSMART = 'SMART' # smart routing

    CurrencyUSD = 'USD'
    CurrencyEUR = 'EUR'

    
    '''
	ticktypeDelayedBidPrice = 66
    ticktypeDelayedAskPrice = 67
    ticktypeDelayedLastPrice = 68 # close
    ticktypeDelayedHighPrice = 72 # high
    ticktypeDelayedLowPrice = 73  # low
    ticktypeDelayedVolume = 74
    ticktypeDelayedOpen = 76      # open. docs say: Not typically available
    '''

    RequestedTickTypes = [76, 68, 72, 73]  # was: [66, 67, 68, 75])
