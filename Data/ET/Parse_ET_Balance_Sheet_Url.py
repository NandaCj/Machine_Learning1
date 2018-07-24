import requests
from lxml.html import fromstring
from bs4 import BeautifulSoup
import re
from Data.From_Db import FindData
from Helpers.Logging import *

Param_Dict = {
            "Share Capital": "Share_Capital",
            "Reserves & Surplus": "Reserves_Surplus",
            "Net Worth": "Net_Worth",
            "Secured Loan": "Secured_Loan",
            "Unsecured Loan": "Unsecured_Loan",
            "TOTAL LIABILITIES": "Total_Liabilities",
            "Gross Block": "Gross_Block",
            "(-) Acc. Depreciation": "Depreciation",
            "Net Block": "Net_Block",
            "Capital Work in Progress": "Capital_Work_In_Progress",
            "Investments": "Investments",
            "Inventories": "Inventories",
            "Sundry Debtors": "Sundry_Debtors",
            "Cash and Bank": "Cash_and_Bank",
            "Loans and Advances": "Loans_And_Advances",
            "Total Current Assets": "Total_Current_Assets",
            "Current Liabilities": "Current_Liabilities",
            "Provisions": "Provisions",
            "Total Current Liabilities": "Total_Current Liabilities",
            "NET CURRENT ASSETS": "Net_Current_Assessts",
            "Misc. Expenses": "Misc_Expenses",
            "TOTAL ASSETS(A+B+C+D+E)":"Total_Assests",
              }

class Parse_Balance_Sheet:

    def __init__(self):
        pass

    def Get_Total_Available_Years_BalaceSheet(self, Balance_Sheet_Page_Soup):
        Balance_Sheet_Years = re.findall(r'Months', Balance_Sheet_Page_Soup.find_all('tr')[3].get_text())
        Years_Of_Detail_avaliable = len(Balance_Sheet_Years)
        Info("Balance Sheet Data if Available for {} years ".format(Years_Of_Detail_avaliable))
        Balance_Sheet_TD = Balance_Sheet_Page_Soup.find_all('tr')[2]
        Years_Of_Detail_avaliable = re.findall(r'Mar...', str(Balance_Sheet_TD))
        Info("Years_Of_Detail_avaliable {}".format(Years_Of_Detail_avaliable))
        return Years_Of_Detail_avaliable

    def Map_Attribute(self, Un_Formated_Attribute):
        Mapped_Attribute_Name = Param_Dict[Un_Formated_Attribute]
        return Mapped_Attribute_Name

    def Five_Years_Data_Parse(self, Stock_Id, Balance_Sheet_Page_Soup, Years_Of_Detail_avaliable,):
        Info("Five Years Data Parse...")
        Share_Capital_Index = 14
        Gross_Block_Index = 51
        Balance_Sheet_TD =  Balance_Sheet_Page_Soup.find_all('td')
        count = 0

        BalanceSheet_Detail_Dict = {"_id":Stock_Id}
        for Year in Years_Of_Detail_avaliable:
            Info("Year :{}".format(Year))
            First_Set_Data = Share_Capital_Index + 1
            Second_Set_Data = Gross_Block_Index + 1
            BalanceSheet_Detail_Dict[Year] = {}
            Info(BalanceSheet_Detail_Dict)
            for Attribute_TD in Balance_Sheet_TD[Share_Capital_Index:Gross_Block_Index-1:6]:
                Attribute = Attribute_TD.get_text()
                Formatted_Attribute_Name = self.Map_Attribute(Attribute)

                for Value_TD in Balance_Sheet_TD[First_Set_Data:First_Set_Data+5][count]:
                    print("Value_TD",Value_TD)
                    # Value = float(Value_TD.get_text())
                    # print("Value", Value)

                    BalanceSheet_Detail_Dict[Year][Formatted_Attribute_Name] = Value_TD


                First_Set_Data += 6
            Info(BalanceSheet_Detail_Dict)
            for Attribute_TD in Balance_Sheet_TD[Gross_Block_Index::6]:
                Attribute = Attribute_TD.get_text()
                Formatted_Attribute_Name = self.Map_Attribute(Attribute)

                for Value_TD in Balance_Sheet_TD[Second_Set_Data:Second_Set_Data+5][count]:
                    Value = float(Value_TD.get_text())
                    BalanceSheet_Detail_Dict[Year][Formatted_Attribute_Name] = Value

                Second_Set_Data += 6

        for key, value in BalanceSheet_Detail_Dict.items():
            print(key ,"********", value)

        return BalanceSheet_Detail_Dict



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
    Obj.Parse_Balance_Sheet_Url(Stock_Id = 'BHEL')