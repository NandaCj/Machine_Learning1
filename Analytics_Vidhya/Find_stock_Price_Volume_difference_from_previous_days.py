from nsetools import Nse
from nsepy import get_history
from datetime import date
from Plot import Matplot
import pandas as pd
import matplotlib.pyplot as plt
nse = Nse()
import pickle
from Helpers import Helpers
from Linear_Regression import Linear_Regression
Feature_List = ['Volume_percent_change', 'HL_PCT', 'Price_Percent_Change']
Label_List = ['Close']
class Price_Volume_Difference:
    def __init__(self):
        pass

    def Prepare_Stock_History_Dataset(self, Stock):
        # History = get_history(symbol=Stock, start=date(2018, 4, 1), end=date(2018, 4, 30))
        # Helpers().Pickle_Dump(History)
        History = Helpers().Pickle_Load()
        History['Price_Percent_Change'] = (History['Close']- History['Open']) / History['Open'] * 100
        History['Volume_percent_change'] = ( History['Volume'] - History['Volume'].shift().fillna(0)) / History['Volume'].shift() * 100
        History['HL_PCT'] = (History['High']- History['Low']) / History['Close'] * 100
        # History.['Label'] =
        History = History.dropna()
        return History



if __name__=="__main__":
    obj = Price_Volume_Difference()
    History = obj.Prepare_Stock_History_Dataset(Stock = 'hdfc')
    print (History.tail()[Feature_List + Label_List])
    #Matplot().Line_Plot("Volume_percent_change", History['Volume_percent_change'], "Price_Percent_Change", History['Price_Percent_Change'])
    import numpy as np

    Feature = np.array(History[Feature_List])
    Label = np.array(History[Label_List])
    #Helpers().Print_Type_And_Value(Feature, Label)
    Linear_Regression().Predict_With_Linear_Regression(Feature, Label)

