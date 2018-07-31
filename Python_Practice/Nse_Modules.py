from nsepy import get_history
from datetime import date
Price_History = get_history(symbol='HDFC', start=date(2018, 1, 1), end=date(2018, 1, 30))
print(Price_History)