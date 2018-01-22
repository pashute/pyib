import sys
import PyIbCaller as pibc


isFromMatlab = True
if isFromMatlab:
    symbol = sys.argv[1]       # "CL"    # ESTX50 # "GBP"
    securityType = sys.argv[2] # "FUT"   # IND    # "CASH"
    currency = sys.argv[3]     # "USD"   # EUR    # "USD"
    exchange = sys.argv[4]     # "NYMEX" # DTB    # "IDEALPRO" 
    monthYYYYMM = ''
else:
    symbol = "ESTX50"
    securityType = "IND"
    currency = "EUR"
    exchange = "DTB"
    monthYYYYMM = ''

print("IB daily info for  {0} {1}-{2}@ {3}".format(symbol, securityType, currency, exchange ))
pibc.GetMktData(symbol, securityType, currency, exchange, monthYYYYMM)

# if __name__ == '__main__':
# symbol       = "CL"  #      ESTX50" # "GBP"
# securityType = "FUT" #   IND"    # "CASH"
# currency     = "USD" #   EUR"    # "USD"
# exchange     = "NYMEX" # DTB"    # "IDEALPRO"
# monthYYYYMM  = "201802"