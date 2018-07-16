from DB import Connection
from nsepy import get_history
from datetime import date

class InsertData:

    def __init__(self):
        self.Db_Client = Connection().Connect
        print("Cursor:", self.Db_Client)

    def Insert_Stock_History(self, Stock = ''):
        cursor = self.Db_Client.Stock_Info.Price_History
        print (cursor)
        Test_Columns = ['High', 'Low']
        Price_History = get_history(symbol=Stock, start=date(2018, 4, 1), end=date(2018, 4, 30))
        print (Price_History.columns.values.tolist())
        print (Price_History.head()[Test_Columns].to_dict('records'))
        cursor.insert({"_id":'Sample', "Inserted From pymongo":"True"})



if __name__ == "__main__":
    Obj = InsertData()
    Obj.Insert_Stock_History('hdfc', )