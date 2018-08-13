from Data.From_Db import FindData
from Helpers.Logging import *
import requests, re, os
from bs4 import BeautifulSoup
from Parsing_Helpers import Parse
import configparser
from Common_Data import Qly_Parm_Dict
from Helpers.Helpers import Stock_Price

Config = configparser.ConfigParser()
Config.read(os.path.dirname(os.path.realpath(__file__)) + "/ET_Config.ini")
INCOME_INDEX = int(Config.get("QLY_SHEET", "INCOME_INDEX"))
NET_SALES_TURNOVER = int(Config.get("QLY_SHEET", "NET_SALES_TURNOVER"))
STOCK_ADJUSTMENT_INDEX = int(Config.get("QLY_SHEET", "STOCK_ADJUSTMENT_INDEX"))
RESERVES_BACK = int(Config.get("QLY_SHEET", "RESERVES_BACK"))


class Parse_Qly_Profit_Loss:

    def __init__(self):
        pass

    def Map_Attribute(self, Un_Formated_Attribute, Dict):
        Mapped_Attribute_Name = Dict[Un_Formated_Attribute]
        return Mapped_Attribute_Name

    def Form_Qly_Detail_Dict(self, Index , count, Qly, Td_Data, From_Td, To_Td, Skip_Td):

        for Attribute_TD in Td_Data[Index::6]:
            Attribute = Attribute_TD.get_text()
            if Attribute == "EXPENSES":
                break
            if Attribute == "KEY ITEMS":
                break
            Formatted_Attribute_Name = self.Map_Attribute(Attribute, Dict=Qly_Parm_Dict)
            if Td_Data[From_Td + count]:
                Value_TD = Td_Data[From_Td + count]
                Value = float(Value_TD.get_text())
                self.Qly_Detail_Dict[Qly][Formatted_Attribute_Name] = Value

            From_Td += 6
            To_Td = From_Td

    def Five_Qly_Data_Parse(self, Stock_Id, Q_Soup, Qly_Months):
        self.Qly_Detail_Dict = {"_id":Stock_Id}
        Qly_Data = Q_Soup.find_all('td') # ALL The Details ?  Wise
        count = 0
        for Qly in Qly_Months:
            Info("Qly : {}".format(Qly))
            First_Set_Data = NET_SALES_TURNOVER + 1 ;  Second_Set_Data = STOCK_ADJUSTMENT_INDEX + 1 ; Third_Set_Data = RESERVES_BACK + 1
            Formated_Qly = str(re.sub("'", "_", Qly))
            Month, Year = Formated_Qly.split("_")
            Close_Price = self.Stock_Price.Get_Close_Price_On_Month_End(Stock_Id=Stock_Id, Month=Month, Year=Year)
            self.Qly_Detail_Dict[Formated_Qly] = {}
            self.Qly_Detail_Dict[Formated_Qly]['Close'] = Close_Price
            self.Form_Qly_Detail_Dict(Index=NET_SALES_TURNOVER, count=count, Qly=Formated_Qly,Td_Data=Qly_Data,
                                               From_Td=First_Set_Data, To_Td=First_Set_Data,Skip_Td=len(Qly_Months))
            Info("Running Second...")
            self.Form_Qly_Detail_Dict(Index=STOCK_ADJUSTMENT_INDEX, count=count, Qly=Formated_Qly, Td_Data=Qly_Data,
                                      From_Td=Second_Set_Data, To_Td=Second_Set_Data + 5, Skip_Td=len(Qly_Months))
            Info("Running Third...")
            self.Form_Qly_Detail_Dict(Index=RESERVES_BACK, count=count, Qly=Formated_Qly, Td_Data=Qly_Data,
                                      From_Td=Third_Set_Data, To_Td=Third_Set_Data + 5, Skip_Td=len(Qly_Months))
            count += 1
        return self.Qly_Detail_Dict

    def Parse_Qly_Url(self, Stock_Id):
        parse = Parse()
        findData = FindData()
        self.Stock_Price = Stock_Price()
        Q_Url = findData.Get_Qly_Url_For_Stock(Stock_Id=Stock_Id)
        Q_Soup = parse.Get_Soup(Q_Url)
        Total_Qs = parse.Get_Qly_Total_Years(Soup = Q_Soup)
        Qly_Months = parse.Get_Qly_Months(Q_Soup)

        if Total_Qs == 5:
            QlyDict = self.Five_Qly_Data_Parse(Stock_Id, Q_Soup, Qly_Months)

        return QlyDict



if __name__ == "__main__":
    print("Parsing Qly Profit Loss Url for Stocks...")
    Obj = Parse_Qly_Profit_Loss()
    Obj.Parse_Qly_Url(Stock_Id='HDFC')
    print (Obj.Qly_Detail_Dict)