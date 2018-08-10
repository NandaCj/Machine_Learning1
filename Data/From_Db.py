from Data.DB import Connection
from nsepy import get_history
from nsetools import Nse
from datetime import date
from datetime import datetime
from Helpers.Logging import *
import re
from datetime import datetime


Test_Columns = ['Symbol', 'Series', 'Prev Close', 'Open', 'High', 'Low', 'Last', 'Close', 'VWAP', 'Volume',
                        'Turnover', 'Trades', 'Deliverable Volume', '%Deliverble']

nse = Nse()

class FindData:

    def __init__(self):
        self.Db_Client = Connection().Connect
        Info("DB Clinet : {}".format(self.Db_Client))

    @property
    def ET_Urls_Cursor(self):
        return self.Db_Client.ET.ETUrls

    @property
    def ET_Urls_Dict(self):
        ET_Urls_Dict = list(self.ET_Urls_Cursor.find({}))[0]
        return ET_Urls_Dict

    @property
    def Get_Balance_Sheet_Details(self):
        cursor = self.Db_Client.Stock_Info.BalanceSheet
        Result = cursor.find({})
        # Result = cursor.find({"_id" : {'$in': ["HDFC", "SBIN"] }})
        #print (list(Result))
        return Result

    @property
    def Get_Qly_Details(self):
        cursor = self.Db_Client.Stock_Info.QlySheet
        Result = cursor.find({}).limit(2)
        # Result = cursor.find({"_id" : {'$in': ["HDFC", "SBIN"] }})
        # print (list(Result))
        return Result

    @property
    def Get_Stock_Split_Url(self):
        cursor = self.Db_Client.ET.ETUrls
        return list(cursor.find({}, {"_id":0, 'StockSplit':1}))[0]['StockSplit']

    def Get_Qly_For_Cols(self, Cols):
        cursor = self.Db_Client.Stock_Info.QlySheet
        Result = cursor.find({}, Cols).limit(2)
        return Result

    def Get_Stock_And_ET_Id_Dict(self, Specific_Stock_Id = False):
        if Specific_Stock_Id:
            Stock_And_ET_Id_Dict = list(self.Db_Client.ET.ETCompanyCodes.find({}, {"_id": 0, Specific_Stock_Id: 1}))[0]
        else:
            Stock_And_ET_Id_Dict = list(self.Db_Client.ET.ETCompanyCodes.find({}))[0]
        Info("Stock_And_ET_Id_Dict : {}".format(Stock_And_ET_Id_Dict))
        return Stock_And_ET_Id_Dict

    def Get_Qly_Url_For_Stock(self, Stock_Id):
        General_Qly_Url = self.ET_Urls_Dict['QuarterlyProfitLoss']
        Stock_And_ET_Id_Dict = self.Get_Stock_And_ET_Id_Dict(Specific_Stock_Id=Stock_Id)
        for Stock_Id, ET_Id in Stock_And_ET_Id_Dict.items():
            Qly_Url_For_Stock = re.sub('Code', ET_Id, General_Qly_Url)
            Info("Qly_Url_For_Stock : {}". format(Qly_Url_For_Stock))
        return Qly_Url_For_Stock

    def Get_Stock_Codes(self):
        Info("Quering Stock Codes...")
        cursor = self.Db_Client.Stock_Info.Stock_List
        stock_list = cursor.find({},{"_id":1})
        for i in stock_list:
            print (i["_id"])

    def Get_Balance_Sheet_General_Url(self):
        Urls = list(self.Db_Client.ET.ETUrls.find({}, {"_id": 0, "BalanceSheet": 1}))
        Info(Urls)
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

    def Get_Missing_Balance_Sheet_Stock_Ids(self):

        ALL = []
        B_IDS = []
        All_Stock_Ids = list(self.Db_Client.Stock_Info.Stock_List.find({},{"_id":1}))
        Balance_Sheet_Ids = list(self.Db_Client.Stock_Info.BalanceSheet.find({},{"_id":1}))
        for id in All_Stock_Ids:
            ALL.append(str(id["_id"]))
        for id in Balance_Sheet_Ids:
            B_IDS.append(str(id["_id"]))


        # print (ALL)
        # print(B_IDS)

        print(len(All_Stock_Ids), len(Balance_Sheet_Ids))
        Diff = list(set(ALL) - set(B_IDS))
        print (Diff)
        print ("Diff:", len(Diff) )


    def Get_Stock_History(self, Stock=None, Start_Date=None, End_Date=None, On_Date=None):
        cursor = self.Db_Client.Stock_Info.Price_History
        if On_Date:

            History = cursor.find({"_id":On_Date}, {Stock+".Close":1, "_id":0})
        # print(list(History))
        return list(History)

if __name__ == "__main__":
    Obj = FindData()
    # Obj.Get_Stock_Codes()
    # Obj.Get_Balance_Sheet_General_Url()
    # Obj.Get_Balance_Sheet_Url_For_Stock(Specific_Stock_Id="BHEL")
    # Obj.Get_Missing_Balance_Sheet_Stock_Ids()

    print(Obj.Get_Stock_History(Stock='3IINFOTECH', On_Date=datetime(2014, 01, 31)))
    # Obj.Get_Stock_History(On_Date='ISODate("2013-03-01T00:00:00.000+0000")')
    # print(Obj.Get_Stock_Split_Url)
