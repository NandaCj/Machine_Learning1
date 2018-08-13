from DB import Connection
from nsepy import get_history
from nsetools import Nse
from datetime import date
from datetime import datetime
from Helpers.Logging import *
from Data.ET.Parse_ET_Balance_Sheet_Url import Parse_Balance_Sheet
from Data.ET.Parse_ET_Quarterly_Result_Url import Parse_Qly_Profit_Loss

Test_Columns = ['Symbol', 'Series', 'Prev Close', 'Open', 'High', 'Low', 'Last', 'Close', 'VWAP', 'Volume',
                        'Turnover', 'Trades', 'Deliverable Volume', '%Deliverble']

nse = Nse()
Errored_Stock_List = ['ITDCEM', 'NESTLEIND', 'TAKE', 'SANOFI', 'SHARONBIO', 'AEGISCHEM', 'ACCELYA',
                      'CRISIL', 'VBL', 'SCHAEFFLER', 'VIDEOIND', 'MERCK', 'PALASHSECU', 'DICIND',
                      'RSYSTEMS', 'ALBERTDAVD', 'AMBUJACEM', 'PAPERPROD', 'MAXVIL', 'GROBTEA', 'TIFIN',
                      'XCHANGING', 'SMSLIFE', 'DCAL', 'GILLETTE', 'LINDEINDIA', 'VARDHACRLC', 'DIGJAMLTD',
                      'RAIN', 'KSBPUMPS', 'HEXAWARE', 'BIGBLOC', 'WSI', 'FOSECOIND', 'ACC', 'SINTEX', 'ABB',
                      'PGHH', 'MAHINDCIE', 'AVADHSUGAR', 'MAGADSUGAR', 'GANGESSECU', 'SIEMENS', 'VESUVIUS',
                      'CASTROLIND']

class InsertData:
    """
    self.Db_Client is Connection Object to Mongo
    access Specific DB by using self.Db_Client.<DB_NAME>.<COLLECTION_NAME>
    """

    def __init__(self):
        self.Db_Client = Connection().Connect
        Info("DB Clinet : {}".format(self.Db_Client))

    def Insert_Stock_History(self, Stock = ''):
        Info("Inserting Trade History for : {}".format(Stock))
        cursor = self.Db_Client.Stock_Info.Price_History
        Price_History = get_history(symbol=Stock, start=date(2013, 1, 1), end=date(2018, 1, 30))

        for index, value in zip(Price_History.index, Price_History.to_dict('records')):
            Date = datetime(year=index.year, month=index.month, day=index.day)
            try:
                cursor.insert({"_id": Date})
            except Exception as err:
                #Critical("Error with Stock :{} \n {}".format(Stock, err))
                pass
            cursor.update({"_id":Date}, {'$set':{Stock:value}})

    def Insert_Stock_Names_List(self):
        cursor = self.Db_Client.Stock_Info.Stock_List
        all_stock_codes = nse.get_stock_codes()
        for StockCode, CompanyName in all_stock_codes.items():
            try :
                cursor.insert({"_id":StockCode , 'Stock_Code':CompanyName})
            except Exception as err:
                Critical("Error in inserting Stock {}".format(StockCode))
                continue

    def Get_Stock_Codes(self):
        pass

    def Insert_Stock_History_All(self):
        Info("Inserting Stock Trade History...")
        cursor = self.Db_Client.Stock_Info.Stock_List
        stock_list = list(cursor.find({}, {"_id": 1}))
        Info("stock_list : {}".format(stock_list))
        for Stock_ID in stock_list[290:]:
            print("{} is in Progress...".format(Stock_ID))
            Stock = Stock_ID["_id"]
            self.Insert_Stock_History(Stock=Stock)

    def Insert_Stock_Balance_Sheet(self, Limit=5):
        BalanceSheetDict = False
        Obj = Parse_Balance_Sheet()
        cursor = self.Db_Client.Stock_Info.Stock_List
        #"_id":{'$in':Errored_Stock_List}
        for Stock_Id in cursor.find({}, {"_id": 1})[:Limit]:
            Stock_Id = Stock_Id["_id"]
            print ("StockId : {}".format(Stock_Id))
            try:
                # Parsing of Url Starts here..
                BalanceSheetDict = Obj.Parse_Balance_Sheet_Url(Stock_Id)
            except Exception as err:
                Critical("Error in initating the Parse Balance Sheet Url... {}".format(err))
            #print (BalanceSheetDict)
            if BalanceSheetDict:
                try:
                    cursor = self.Db_Client.Stock_Info.BalanceSheet
                    cursor.insert(BalanceSheetDict)
                except Exception as err:
                    Critical(err)
                    Critical("Error in Inserting the Data to DB ...")

            else:
                Critical("{} Balance Sheet Details are not added in DB".format(Stock_Id))

    def Insert_Qly_Profit_Loss(self, Limit=5):
        QlyDict = False
        Obj = Parse_Qly_Profit_Loss()
        cursor = self.Db_Client.Stock_Info.Stock_List
        #"_id":{'$in':Errored_Stock_List}
        for Stock_Id in cursor.find({}, {"_id": 1})[:Limit]:
            Stock_Id = Stock_Id["_id"]
            print ("StockId : {}".format(Stock_Id))
            try:
                # Parsing of Url Starts here..
                QlyDict = Obj.Parse_Qly_Url(Stock_Id)
            except Exception as err:
                Critical("Error in initating the Parse Balance Sheet Url... {}".format(err))
            #print (BalanceSheetDict)
            if QlyDict:
                try:
                    cursor = self.Db_Client.Stock_Info.QlySheet
                    cursor.insert(QlyDict)
                except Exception as err:
                    Critical(err)
                    Critical("Error in Inserting the Data to DB ...")

            else:
                Critical("{} Balance Sheet Details are not added in DB".format(Stock_Id))

if __name__ == "__main__":
    Obj = InsertData()
    # Obj.Insert_Stock_Balance_Sheet(Limit=2000)
    # Obj.Insert_Stock_Names_List()
    # Obj.Insert_Stock_History_All()
    Obj.Insert_Qly_Profit_Loss(Limit=20)