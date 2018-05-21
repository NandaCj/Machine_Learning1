from nsetools import Nse
from nsepy import get_history
from datetime import date
from Plot import Matplot
import pandas as pd
import matplotlib.pyplot as plt
nse = Nse()
import pickle
from Helpers import Helpers

class Price_Volume_Difference:
    def __init__(self):
        pass

    def Prepare_Stock_History_Dataset(self, Stock):
        History = get_history(symbol=Stock, start=date(2018, 4, 1), end=date(2018, 4, 30))
        Helpers().Pickle_Dump(History)
        History = Helpers().Pickle_Load()
        History['Price_Percent_Change'] = (History['Close']- History['Prev Close']) / History['Close'] * 100
        History['Volume_percent_change'] = ( History['Volume'] - History['Volume'].shift().fillna(0)) / History['Volume'].shift() * 100
        History = History.dropna()
        return History



if __name__=="__main__":
    obj = Price_Volume_Difference()
    History = obj.Prepare_Stock_History_Dataset(Stock = 'hdfc')
    print (History)
    Matplot().Line_Plot("Volume_percent_change", History['Volume_percent_change'], "Price_Percent_Change", History['Price_Percent_Change'])


