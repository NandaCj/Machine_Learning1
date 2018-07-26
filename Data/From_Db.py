from Data.DB import Connection
from nsepy import get_history
from nsetools import Nse
from datetime import date
from datetime import datetime
from Helpers.Logging import *
import re


Test_Columns = ['Symbol', 'Series', 'Prev Close', 'Open', 'High', 'Low', 'Last', 'Close', 'VWAP', 'Volume',
                        'Turnover', 'Trades', 'Deliverable Volume', '%Deliverble']

nse = Nse()

class FindData:

    def __init__(self):
        self.Db_Client = Connection().Connect
        Info("DB Clinet : {}".format(self.Db_Client))

    @property
    def Get_Balance_Sheet_Details(self):
        cursor = self.Db_Client.Stock_Info.BalanceSheet

        Result = cursor.find({"_id" : {'$in': ["HDFC", "SBIN"] }})
        #print (list(Result))
        return Result


    def Get_Stock_Codes(self):
        Info("Quering Stock Codes...")
        cursor = self.Db_Client.Stock_Info.Stock_List
        stock_list = cursor.find({},{"_id":1})
        for i in stock_list:
            print (i["_id"])

    def Get_Balance_Sheet_General_Url(self):
        Urls = list(self.Db_Client.ET.ETUrls.find({}, {"_id": 0, "BalanceSheet": 1}))
        General_Balance_Sheet_Url = Urls[0]['BalanceSheet']
        # Info("BalanceSheetUrl : {}".format(General_Balance_Sheet_Url))

        return General_Balance_Sheet_Url

    def Get_Balance_Sheet_Url_For_Stock(self, Specific_Stock_Id = False):
        if Specific_Stock_Id:
            Stock_And_ET_Id_Dict = list(self.Db_Client.ET.ETCompanyCodes.find({}, {"_id": 0, Specific_Stock_Id: 1}))[0]
        else:
            Stock_And_ET_Id_Dict = list(self.Db_Client.ET.ETCompanyCodes.find({}))[0]

        return Stock_And_ET_Id_Dict

    def Get_ET_Id_Missing_Stock_Ids(self):
        pass


if __name__ == "__main__":
    Obj = FindData()
    # Obj.Get_Stock_Codes()
    # Obj.Get_Balance_Sheet_General_Url()
    # Obj.Get_Balance_Sheet_Url_For_Stock(Specific_Stock_Id="BHEL")