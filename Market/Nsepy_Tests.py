import nsepy
from nsepy import get_history
from datetime import date

# data = get_history(symbol="SBIN", start=date(2018,5,3), end=date(2018,5,4))
nifty_next50 = get_history(symbol="NIFTY 50",start=date(2018,10,17),end=date(2018,10,17),index=True)

print(nifty_next50)
print(nifty_next50['Close'])
