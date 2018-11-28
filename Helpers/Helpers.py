import pickle
import logging
import numpy as np
from pandas.tseries.offsets import BMonthEnd
from datetime import datetime as dt
from datetime import date, timedelta
from nsepy import get_history

Log_Format = "%(asctime)s %(levelname)s [%(name)s] %(message)s"
logging.basicConfig(level='CRITICAL', format=Log_Format)
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

    def Qly_Increasing_Order(self, Qlys):
        Q_str_Dt_Dict = {}
        for Q_str in Qlys:
            month , year = Q_str.split("_")
            Q_dt = self.Last_Working_Day('01', month, year)
            Q_str_Dt_Dict[Q_str] = Q_dt # {"Mar_18" : Timestamp('2018-03-30 00:00:00')}

        Q_dt_list = Q_str_Dt_Dict.values() # [Timestamp('2017-09-29 00:00:00'), Timestamp('2018-03-30 00:00:00'), Timestamp('2017-06-30 00:00:00'), Timestamp('2017-12-29 00:00:00'), Timestamp('2017-03-31 00:00:00')]
        Ord_Qlys = []
        for Q_dt in sorted(Q_dt_list)[::-1]:
            for key, value in Q_str_Dt_Dict.iteritems():
                if value == Q_dt:
                    Ord_Qlys.append(key)

        # With_Alias_Ordered_Q_str = {'Q'+ num : i for num , i in  {num , i for num , i in zip(Ordered_Q_str, range(1, len(Ordered_Q_str) + 1))}}
        Ord_Qlys_alias = {}
        for Qly in Ord_Qlys:
            Ord_Qlys_alias[Qly] = 'RQ_' + str(Ord_Qlys.index(Qly) + 1)

        Info("Qlys              :{}".format(Qlys))
        Info("Ord_Qlys          :{}".format(Ord_Qlys))
        Info("Ord_Qlys_alias    :{}".format(Ord_Qlys_alias))
        """
        Sample :
        Input :
            [u'Jun_17', u'Sep_17', u'Dec_17', u'Mar_17', u'Mar_18']
        Output :
            [u'Mar_18', u'Dec_17', u'Sep_17', u'Jun_17', u'Mar_17']
            {u'Sep_17': 'RQ_3', u'Mar_18': 'RQ_1', u'Jun_17': 'RQ_4', u'Dec_17': 'RQ_2', u'Mar_17': 'RQ_5'}    
        
        """
        return Ord_Qlys, Ord_Qlys_alias




class Stock_Price:

    def __init__(self):
        pass

    def Get_Close_Price_On_Date(self, Stock_Id='fconsumer', Date=dt.strptime('9-Aug-18', '%d-%b-%y')):
        S_Date = date(Date.year, Date.month, Date.day)
        try:
            Info("Getting Close Price on {}".format(S_Date))
            Close_Price = get_history(symbol=Stock_Id, start=S_Date, end=S_Date)['Close'].get_values()[0]
            Prev_Close = get_history(symbol=Stock_Id, start=S_Date, end=S_Date)['Prev Close'].get_values()[0]

        except Exception as err:
            Critical(err)
            Critical("No Close Price for this month Hence Returing 0 ")
            return 0

        Info("{} Close Price on {} = {}".format(Stock_Id, S_Date, Close_Price))
        return Close_Price, Prev_Close

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


class Print_Helpers:

    def Decorate_And_Print(self, Print_This):
        print("---------------------------------------")
        print("|", Print_This, '|')
        print("---------------------------------------")





if __name__ == "__main__":
    Obj = Date_Helpers()
    Obj.Qly_Increasing_Order([u'Jun_17', u'Sep_17', u'Dec_17', u'Mar_17', u'Mar_18'])
    # LDate = Obj.Last_Working_Day(month='Sep', year='18'); print(LDate)
    # Obj.Previous_Working_Day(Date=LDate)
    # Obj.First_Working_Day(month='Sep', year='17')
    # Obj = Stock_Price()
    # Obj.Get_Close_Price_On_Date()
    # Obj.Get_Close_Price_On_Month_End(Stock_Id='FRETAIL', Month='Mar', Year='18')
