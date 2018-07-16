from DB import Connection
from nsepy import get_history
from nsetools import Nse
from datetime import date
from datetime import datetime
from Helpers.Logging import *

Test_Columns = ['Symbol', 'Series', 'Prev Close', 'Open', 'High', 'Low', 'Last', 'Close', 'VWAP', 'Volume',
                        'Turnover', 'Trades', 'Deliverable Volume', '%Deliverble']

nse = Nse()

class InsertData:

    def __init__(self):
        self.Db_Client = Connection().Connect
        Info("DB Clinet : {}".format(self.Db_Client))

    def Insert_Stock_History(self, Stock = ''):
        Info("Inserting Trade History for : {}".format(Stock))
        cursor = self.Db_Client.Stock_Info.Price_History
        Price_History = get_history(symbol=Stock, start=date(2018, 4, 1), end=date(2018, 4, 30))

        for index, value in zip(Price_History.index, Price_History.to_dict('records')):
            cursor.insert({"_id": Date})
            Date = datetime(year=index.year, month=index.month, day=index.day)
            cursor.update({"_id":Date}, {'$set':{Stock:value}})

    def Insert_Stock_Names_List(self):
        cursor = self.Db_Client.Stock_Info.Stock_List
        all_stock_codes = nse.get_stock_codes()
        for StockCode, CompanyName in all_stock_codes.items():
            cursor.insert({"_id":StockCode , 'Stock_Code':CompanyName})

    def Get_Stock_Codes(self):
        pass

    def Insert_Stock_History_All(self):
        Info("Inserting Stock Trade History...")
        cursor = self.Db_Client.Stock_Info.Stock_List
        stock_list = cursor.find({}, {"_id": 1})
        for Stock_ID in stock_list[:5]:
            Stock = Stock_ID["_id"]
            self.Insert_Stock_History(Stock=Stock)


if __name__ == "__main__":
    Obj = InsertData()
    # Obj.Insert_Stock_History('hdfc', )
    #Obj.Get_Stock_Names_List()
    Obj.Insert_Stock_History_All()