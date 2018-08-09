import pickle
import logging
import numpy as np
from pandas.tseries.offsets import BMonthEnd
from datetime import datetime as dt
from datetime import date, timedelta
from nsepy import get_history

Log_Format = "%(asctime)s %(levelname)s [%(name)s] %(message)s"
logging.basicConfig(level='DEBUG', format=Log_Format)
logger = logging.getLogger(__name__)
Info = logger.info
Critical = logger.critical

Pickle_File = "Pickle_Dump"

class Helpers:

    def __init__(self):
        pass

    def Print_Type_And_Value(self, *args):
        print("************************************************")
        for arg in args:

            print ("Total Length of Argument : ", len(arg))
            print ("Argument Type :", type(arg), "\n")
            if isinstance(arg, (np.ndarray)):
                print ("--->Array Shape ", arg.shape)
            print ("Argument Value :", arg, "\n")
        print ("************************************************")

    def Pickle_Dump (self, Object_To_Dump):
        File_Object = open(Pickle_File, "wb")
        pickle.dump(Object_To_Dump, File_Object)

    def Pickle_Load (self):
        File_Object = open(Pickle_File, "rb")
        Loaded_Object = pickle.load(File_Object)

        return Loaded_Object

class StartLogging:

    def __init__(self, log_level='DEBUG'):
        logging.basicConfig(level=log_level)
        logger = logging.getLogger(log_level)
        global Info
        Info = logger.info


class Date_Helpers:

    def __init__(self):
        pass

    def Last_Working_Day(self, day='01', month='', year=''):
        Date = day+"-"+month+"-"+year
        LastDay = BMonthEnd().rollforward(dt.strptime(Date, '%d-%b-%y'))
        return LastDay


    def First_Working_Day(self, day='01', month='', year=''):
        Date = day + "-" + month + "-" + year
        FirstDay = BMonthEnd().rollback(dt.strptime(Date, '%d-%b-%y'))
        return FirstDay

    def Previous_Working_Day(self, Date):
        PDate = Date - timedelta(days=10)
        if PDate.weekday() not in range(1,6):
            self.Previous_Working_Day(PDate)
        return PDate


class Stock_Price:

    def __init__(self):
        pass

    def Get_Close_Price_On_Date(self, Stock_Id='fconsumer', Date=dt.strptime('9-Aug-18', '%d-%b-%y')):
        S_Date = date(Date.year, Date.month, Date.day)
        try:
            Info("Getting Close Price on {}".format(S_Date))
            Close_Price = get_history(symbol=Stock_Id, start=S_Date, end=S_Date)['Close'].get_values()[0]
        except Exception as err:
            Critical(err)
            Critical("No Close Price for this month Hence Returing 0 ")
            return 0

        Info("{} Close Price on {} = {}".format(Stock_Id, S_Date, Close_Price))
        return Close_Price

    def Get_Close_Price_On_Month_End(self, Stock_Id='', Month='', Year = ''):
        LDate = Date_Helpers().Last_Working_Day(month=Month, year=Year)
        CPrice = self.Get_Close_Price_On_Date(Stock_Id=Stock_Id, Date=LDate)
        tries = 0
        if CPrice == 0 and tries < 5:
            LDate = LDate - timedelta(days=2)
            if LDate.weekday() in [0,6]:
                LDate = LDate - timedelta(days=2)
            CPrice = self.Get_Close_Price_On_Date(Stock_Id=Stock_Id, Date=LDate)
            tries += 1

        return CPrice









if __name__ == "__main__":
    # Obj = Date_Helpers()
    # LDate = Obj.Last_Working_Day(month='Sep', year='18'); print(LDate)
    # Obj.Previous_Working_Day(Date=LDate)
    # Obj.First_Working_Day(month='Sep', year='17')
    Obj = Stock_Price()
    # Obj.Get_Close_Price_On_Date()
    Obj.Get_Close_Price_On_Month_End(Stock_Id='FRETAIL', Month='Mar', Year='18')