import requests
from lxml.html import fromstring
from bs4 import BeautifulSoup
import re, os
from Data.From_Db import FindData
from Helpers.Logging import *
from Common_Data import BalanceSheet_Param_Dict, BalanceSheet_March_Dict
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

    def Map_Attribute(self, Un_Formated_Attribute, Dict):
        Mapped_Attribute_Name = Dict[Un_Formated_Attribute]
        return Mapped_Attribute_Name

    def Map_March(self, Year):
        if '13' in Year:return "Mar_13"
        if '14' in Year: return "Mar_14"
        if '15' in Year: return "Mar_15"
        if '16' in Year: return "Mar_16"
        if '17' in Year:return "Mar_17"
        if '18' in Year: return "Mar_18"
        if '19' in Year:return "Mar_19"


    def Form_BalanceSheet_Detail_Dict(self, Index , count, Year, Balance_Sheet_Table_Data, From_Td, To_Td, Skip_Td):
        global SHARE_CAPITAL_INDEX

        for Attribute_TD in Balance_Sheet_Table_Data[Index::6]:

            Info("self.BalanceSheet_Detail_Dict : {}".format(self.BalanceSheet_Detail_Dict))
            Info("Attribute_TD : {} , SHARE_CAPITAL_INDEX: {}".format(Attribute_TD, SHARE_CAPITAL_INDEX))
            Attribute = Attribute_TD.get_text()
            if Attribute == "Assets":

                #SHARE_CAPITAL_INDEX = GROSS_BLOCK_INDEX
                Info("**************** Continue *****************")
                break
            Formatted_Attribute_Name = self.Map_Attribute(Attribute, Dict=BalanceSheet_Param_Dict)
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
            Formated_Year = self.Map_March(Year)
            self.BalanceSheet_Detail_Dict[Formated_Year] = {}
            self.Form_BalanceSheet_Detail_Dict(Index = SHARE_CAPITAL_INDEX, count=count, Year=Formated_Year, Balance_Sheet_Table_Data= Balance_Sheet_Table_Data,
                                               From_Td=First_Set_Data, To_Td=First_Set_Data, Skip_Td=len(Years_Of_Detail_avaliable))

            Info("Running Second...")
            self.Form_BalanceSheet_Detail_Dict(Index=GROSS_BLOCK_INDEX, count=count, Year=Formated_Year, Balance_Sheet_Table_Data=Balance_Sheet_Table_Data,
                                               From_Td=Second_Set_Data, To_Td=Second_Set_Data + 5,Skip_Td=len(Years_Of_Detail_avaliable))
            count += 1
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

        # for key, value in self.BalanceSheet_Detail_Dict.items():
        #     print(key ,"********", value)

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
        BalanceSheet_Detail_Dict = False
        FindData_Obj = FindData()
        General_Balance_Sheet_Url = FindData_Obj.Get_Balance_Sheet_General_Url()
        Stock_And_ET_Id_Dict = FindData_Obj.Get_Balance_Sheet_Url_For_Stock(Specific_Stock_Id=Stock_Id)
        for Stock_Id, ET_Id in Stock_And_ET_Id_Dict.items():
            Balance_Sheet_Url_For_Stock = re.sub('Code', ET_Id, General_Balance_Sheet_Url)
            print("Balance_Sheet_Url_For_Stock : {}". format(Balance_Sheet_Url_For_Stock))

            try:
                BalanceSheet_Detail_Dict = self.Parse_Balance_Sheet_Details(Stock_Id, Balance_Sheet_Url_For_Stock)
            except:
                Critical("Error in Parsing Stock_ID : {}".format(Stock_Id))
                return False
        return BalanceSheet_Detail_Dict


if __name__ == "__main__":
    Obj = Parse_Balance_Sheet()
    Obj.Parse_Balance_Sheet_Url(Stock_Id = 'HDFC')