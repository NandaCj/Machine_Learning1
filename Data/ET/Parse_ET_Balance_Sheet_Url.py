import requests
from lxml.html import fromstring
from bs4 import BeautifulSoup
import re, os
from Data.From_Db import FindData
from Helpers.Logging import *
from Common_Data import BalanceSheet_Param_Dict
import configparser


Config = configparser.ConfigParser()
Config.read(os.path.dirname(os.path.realpath(__file__)) + "/ET_Config.ini")
SHARE_CAPITAL_INDEX = int(Config.get("BALANCE_SHEET", "SHARE_CAPITAL_INDEX"))
GROSS_BLOCK_INDEX = int(Config.get("BALANCE_SHEET", "GROSS_BLOCK_INDEX"))

class Parse_Balance_Sheet:

    def __init__(self):
        pass

    def Get_Total_Available_Years_BalaceSheet(self, Balance_Sheet_Page_Soup):
        Balance_Sheet_Years = re.findall(r'Months', Balance_Sheet_Page_Soup.find_all('tr')[3].get_text())
        Years_Of_Detail_avaliable = len(Balance_Sheet_Years)
        Info("Balance Sheet Data if Available for {} years ".format(Years_Of_Detail_avaliable))
        Balance_Sheet_Table_Data = Balance_Sheet_Page_Soup.find_all('tr')[2]
        Years_Of_Detail_avaliable = re.findall(r'Mar...', str(Balance_Sheet_Table_Data))
        Info("Years_Of_Detail_avaliable {}".format(Years_Of_Detail_avaliable))
        return Years_Of_Detail_avaliable

    def Map_Attribute(self, Un_Formated_Attribute):
        Mapped_Attribute_Name = BalanceSheet_Param_Dict[Un_Formated_Attribute]
        return Mapped_Attribute_Name

    def Form_BalanceSheet_Detail_Dict(self, count, Year, Balance_Sheet_Table_Data, From_Td, To_Td, Skip_Td):
        global SHARE_CAPITAL_INDEX

        for Attribute_TD in Balance_Sheet_Table_Data[SHARE_CAPITAL_INDEX::6]:

            Info("self.BalanceSheet_Detail_Dict : {}".format(self.BalanceSheet_Detail_Dict))
            Info("Attribute_TD : {} , SHARE_CAPITAL_INDEX: {}".format(Attribute_TD, SHARE_CAPITAL_INDEX))
            Attribute = Attribute_TD.get_text()
            if Attribute == "Assets":

                #SHARE_CAPITAL_INDEX = GROSS_BLOCK_INDEX
                Info("**************** Continue *****************")
                break
            Formatted_Attribute_Name = self.Map_Attribute(Attribute)
            Info("Formatted_Attribute_Name : {}".format(Formatted_Attribute_Name))
            Info("From_Td : {} , To_Td : {} , Count : {}".format(From_Td, To_Td, count))
            if Balance_Sheet_Table_Data[From_Td + count]:
                Value_TD = Balance_Sheet_Table_Data[From_Td + count]
                Info("Value_TD : {}".format(Value_TD))
                Value = float(Value_TD.get_text())
                Info("Value : {}".format(Value))

                self.BalanceSheet_Detail_Dict[Year][Formatted_Attribute_Name] = Value

            From_Td += 6
            To_Td = From_Td


    def Five_Years_Data_Parse(self, Stock_Id, Balance_Sheet_Page_Soup, Years_Of_Detail_avaliable,):
        Balance_Sheet_Table_Data =  Balance_Sheet_Page_Soup.find_all('td')
        count = 0
        self.BalanceSheet_Detail_Dict = {"_id":Stock_Id}
        count = 0
        for Year in Years_Of_Detail_avaliable:
            Info("Year :{}".format(Year))
            First_Set_Data = SHARE_CAPITAL_INDEX + 1
            Second_Set_Data = GROSS_BLOCK_INDEX + 1
            self.BalanceSheet_Detail_Dict[Year] = {}
            self.Form_BalanceSheet_Detail_Dict(count=count, Year=Year, Balance_Sheet_Table_Data= Balance_Sheet_Table_Data,
                                               From_Td=First_Set_Data, To_Td=First_Set_Data, Skip_Td=len(Years_Of_Detail_avaliable))
            count += 1
            # self.Form_BalanceSheet_Detail_Dict(Year=Year, Balance_Sheet_Table_Data=Balance_Sheet_Table_Data,
            #                                    From_Td=First_Set_Data, To_Td=First_Set_Data + 5,Skip_Td=len(Years_Of_Detail_avaliable))
            # for Attribute_TD in Balance_Sheet_Table_Data[SHARE_CAPITAL_INDEX:GROSS_BLOCK_INDEX-1:6]:
            #     Attribute = Attribute_TD.get_text()
            #     Formatted_Attribute_Name = self.Map_Attribute(Attribute)
            #
            #     for Value_TD in Balance_Sheet_Table_Data[First_Set_Data:First_Set_Data+5][count]:
            #         print("Value_TD",Value_TD)
            #         Value = float(Value_TD.get_text())
            #         print("Value", Value)
            #
            #         self.BalanceSheet_Detail_Dict[Year][Formatted_Attribute_Name] = Value_TD
            #
            #
            #     First_Set_Data += 6
            # Info(self.BalanceSheet_Detail_Dict)
            # for Attribute_TD in Balance_Sheet_Table_Data[GROSS_BLOCK_INDEX::6]:
            #     Attribute = Attribute_TD.get_text()
            #     Formatted_Attribute_Name = self.Map_Attribute(Attribute)
            #
            #     for Value_TD in Balance_Sheet_Table_Data[Second_Set_Data:Second_Set_Data+5][count]:
            #         Value = float(Value_TD.get_text())
            #         self.BalanceSheet_Detail_Dict[Year][Formatted_Attribute_Name] = Value
            #
            #     Second_Set_Data += 6

        for key, value in self.BalanceSheet_Detail_Dict.items():
            print(key ,"********", value)

        return self.BalanceSheet_Detail_Dict



    def Parse_Balance_Sheet_Details(self, Stock_Id, Balance_Sheet_Url_For_Stock):
        Balance_Sheet_Page = requests.get(Balance_Sheet_Url_For_Stock).text
        Balance_Sheet_Page_Soup = BeautifulSoup(Balance_Sheet_Page, 'html.parser')
        Years_Of_Detail_avaliable = self.Get_Total_Available_Years_BalaceSheet(Balance_Sheet_Page_Soup)


        # for Row_Wise_Data in Balance_Sheet_Page_Soup.find_all('tr').text: # Gets the Row_Wise Data from the Balance Sheet Table
        # if Years_Of_Detail_avaliable == 5:
        BalanceSheet_Detail_Dict = self.Five_Years_Data_Parse(Stock_Id, Balance_Sheet_Page_Soup, Years_Of_Detail_avaliable)
        return BalanceSheet_Detail_Dict

    def Parse_Balance_Sheet_Url(self, Stock_Id):
        FindData_Obj = FindData()
        General_Balance_Sheet_Url = FindData_Obj.Get_Balance_Sheet_General_Url()
        Stock_And_ET_Id_Dict = FindData_Obj.Get_Balance_Sheet_Url_For_Stock(Specific_Stock_Id=Stock_Id)
        for Stock_Id, ET_Id in Stock_And_ET_Id_Dict.items():
            Balance_Sheet_Url_For_Stock = re.sub('Code', ET_Id, General_Balance_Sheet_Url)
            Info("Balance_Sheet_Url_For_Stock : {}". format(Balance_Sheet_Url_For_Stock))
            BalanceSheet_Detail_Dict = self.Parse_Balance_Sheet_Details(Stock_Id, Balance_Sheet_Url_For_Stock)
        return BalanceSheet_Detail_Dict


if __name__ == "__main__":
    Obj = Parse_Balance_Sheet()
    Obj.Parse_Balance_Sheet_Url(Stock_Id = 'HDFC')