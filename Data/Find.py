from DB import Connection
from nsepy import get_history
from nsetools import Nse
from datetime import date
from datetime import datetime
from Helpers.Logging import *

Test_Columns = ['Symbol', 'Series', 'Prev Close', 'Open', 'High', 'Low', 'Last', 'Close', 'VWAP', 'Volume',
                        'Turnover', 'Trades', 'Deliverable Volume', '%Deliverble']

nse = Nse()

class FindData:

    def __init__(self):
        self.Db_Client = Connection().Connect
        Info("DB Clinet : {}".format(self.Db_Client))


    def Get_Stock_Codes(self):
        Info("Quering Stock Codes...")
        cursor = self.Db_Client.Stock_Info.Stock_List
        stock_list = cursor.find({},{"_id":1})
        for i in stock_list:
            print (i["_id"])


if __name__ == "__main__":
    Obj = FindData()
    Obj.Get_Stock_Codes()