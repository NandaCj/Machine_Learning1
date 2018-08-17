from sklearn import linear_model
import pandas as pd
import numpy as np
from Helpers.Logging import *
from Helpers.Helpers import Helpers
from Data.From_Db import FindData
import matplotlib.pyplot as plt
from Pandas_Practice.Pandas_Helpers import Df_view
from Helpers.Helpers import Date_Helpers
import time
from Data.ET.Common_Data import BalanceSheet_March_Dict, BalanceSheet_Param_Dict
import os, re
from datetime import datetime
from pandas.tseries.offsets import BMonthEnd
Filler = "****************************************************************"
Req_Qly_Cols = ['PAT', 'Operating_Profit', 'Total_Exp', 'Ebit', 'Ebitda', 'Close']
# Req_Qly_Cols = ['PAT', 'Close']

class Linear_Regression:

    def __init__(self):
        pass

    def Make_BalanceSheet_Dataframe(self, BalanceSheet_Detail_For_All_Stock, ):
        Info(Filler)
        Different_Format_Stocks = []
        Stock = ""
        BalanceSheet_Dict = {}
        df_Columns = []
        BalanceSheet_df = None
        for Each_Stock_BalanceSheet_Data in BalanceSheet_Detail_For_All_Stock:
            #[ {"_id":"HDFC"},
            # {'Mar_17' : {'Net_Worth':100, 'Capital': 40, etc ...},
            # {'Mar_18' : {'Net_Worth':140, 'Capital': 50, etc ...},]
            try:
                Stock = str(Each_Stock_BalanceSheet_Data["_id"])  # HDFC
                BalanceSheet_Dict[Stock] = {} # {'HDFC' : {}}
                for Each_Quarter in Each_Stock_BalanceSheet_Data.keys(): # ['Mar_17', 'Mar_18']
                    if Each_Quarter == "_id": #{"_id":"HDFC"}
                        continue
                    for Each_Attr in Each_Stock_BalanceSheet_Data[Each_Quarter].keys():#['Net_Worth', 'Capital'] for Mar_17
                        BalanceSheet_Attr_Value = Each_Stock_BalanceSheet_Data[Each_Quarter][Each_Attr] # 100
                        BalanceSheet_Attr = Each_Quarter + "_" + Each_Attr # Mar_17_Net_Worth


                        BalanceSheet_Dict[Stock][BalanceSheet_Attr] = BalanceSheet_Attr_Value # {'HDFC':{'Mar_17_Net_Worth':100}}
                        df_Columns.append(BalanceSheet_Attr)
                Info("Generated Balance Sheet Dataframe for {}".format(Stock))
            except Exception as err:
                Critical(err)
                Different_Format_Stocks.append(Stock)
        BalanceSheet_df = pd.DataFrame.from_dict(BalanceSheet_Dict, orient="index")
        BalanceSheet_df = BalanceSheet_df.sort_index(axis=1, ascending=False) # to Sort the Columns increasing on Yearly 
        # Critical("Total {} Stocks have Different Format of BalaceSheet Details in Economic Times".format(len(Different_Format_Stocks)))
        # Critical(Different_Format_Stocks)

        return BalanceSheet_df


    def Get_BalanceSheet_Data_For_Linear_Regression(self, from_csv = False, csv='None'):
        if from_csv :
            Info("Genearting BalanceSheet Dataframe from CSV {}".format(CSV_PATH_ORG))
            BalanceSheet_df = pd.DataFrame.from_csv(path=CSV_PATH_ORG)
            return BalanceSheet_df
        BalanceSheet_Details_From_DB = list(FindData().Get_Balance_Sheet_Details)
        BalanceSheet_df = self.Make_BalanceSheet_Dataframe(BalanceSheet_Details_From_DB)

        return BalanceSheet_df



    def Yearly_BalanceSheet_Param_Change_Percent(self, BalanceSheet_Df=None):

        """
            BalanceSheet_Df:
                    Mar_16_Net_Worth    Mar_16_Capital  Mar_17_Net_Worth    Mar_17_Capital  Dec_17_Net_Worth
            HDFC        100                 40              140                 50              NaN
            SBIN        200                 50              300                 60              NaN

        Note : The BalanceSheet_Df has some Quarters Columns which are have no Data for that Quarter those needs to reomved...
        """

        BalanceSheet_Param_PChg_Df = pd.DataFrame() # For Storing all Stocks BalaceSheet DFs in Singe DFs
        for index in BalanceSheet_Df.index:
            New_DF = pd.DataFrame() # Create New BalaceSheet Df for each Stock
            All_Quarter_And_Values = [] # ['Mar_16_Net_Worth', 'Mar_17_Net_Worth', etc...]
            try:
                tmp_df = BalanceSheet_Df.loc[[index]].dropna(axis='columns') # drop complete Quarter Columns in BalanceSheet_Df is it has even 1 missing value
            except Exception as err:
                Critical(err)
                Critical("{} has issue in this Dataframe".format(index))
                continue
            for column in tmp_df.columns:
                All_Quarter_And_Values.append(column)
            Sorted_Quarters = sorted(set([q[:6] for q in sorted(All_Quarter_And_Values)])) # ['Mar_16', Mar_17, ...]
            for i in range(len(Sorted_Quarters) - 1):
                Quarter = Sorted_Quarters[i][:3]  # Mar_
                L_Year = Sorted_Quarters[i][4:6]  # 16
                H_Year = Sorted_Quarters[i + 1][4:6] # 17
                for attr in BalanceSheet_Param_Dict.values():
                    New_attr = Quarter + "_" + L_Year + "_" + H_Year + "_" + attr + "_PChg" # Mar_16_17_Net_Worth_Pchg
                    L_Column = Quarter + "_" + L_Year + "_" + attr # Mar_16_Net_Worth
                    H_Column = Quarter + "_" + H_Year + "_" + attr # Mar_17_Net_Worth
                    try:
                        New_DF[New_attr] = ((tmp_df[H_Column] - tmp_df[L_Column]) / tmp_df[L_Column]) * 100
                    except KeyError:
                        Critical("{} does not have this key...".format(index))
                        continue
            Info("calculated for {}".format(index))
            BalanceSheet_Param_PChg_Df = BalanceSheet_Param_PChg_Df.append(New_DF) # This is done bcoz we need a New_DF created for Each Stock

        return BalanceSheet_Param_PChg_Df

    def Yearly_Stock_Price_Change_Percent(self, BalanceSheet_Param_PChg_Df):

        find_data = FindData()
        """
                    BalanceSheet_Param_PChg_Df:
                            Mar_16_17_Net_Worth_PChg    Mar_16_17_Capital_PChg
                    HDFC        45                              25
                    SBIN        26                              10

                Note : The BalanceSheet_Param_PChg_Df has some Quarters Columns which are have no Data for that Quarter those needs to reomved...
        """


        for index in BalanceSheet_Param_PChg_Df.index:
            try:
                tmp_df = BalanceSheet_Param_PChg_Df.loc[[index]].dropna(axis='columns')
            except:
                Critical("{} has issue in this Dataframe".format(index))
                continue
            All_Quarter_And_Values = []
            for column in tmp_df.columns:
                All_Quarter_And_Values.append(column)
            Sorted_Years_Chg = sorted(set([q[:9] for q in sorted(All_Quarter_And_Values)])) # ['Mar_16_17', Mar_17_18, ...]
            Years = re.findall(r'\d+', " ".join(Sorted_Years_Chg)) # ['16', '17']
            Quarter = All_Quarter_And_Values[2][:3] # Mar
            Sorted_Years = sorted(set(Years))
            for i in range(len(set(Years)) - 1):
                F_Year = '20'+Sorted_Years[i] # 2016
                S_Year = '20'+Sorted_Years[i+1] # 2017
                New_Attr = Quarter +"_"+ Sorted_Years[i] +"_"+Sorted_Years[i+1]+"_Stock_Price_PChg" # Mar_16_17_Stock_Price_PChg
                F_Date = datetime(int(F_Year), 1, 4) # 2016, Jan, 4
                S_Date = datetime(int(S_Year), 1, 4) # 2017, Jan, 4
                F_Date = BMonthEnd().rollforward(F_Date) # Last Working Date in 2016 Jan month
                S_Date = BMonthEnd().rollforward(S_Date) # Last Working Date in 2017 Jan month
                try:
                    F_Stock_Price = find_data.Get_Stock_History(Stock=index, On_Date=F_Date)
                    S_Stock_Price = find_data.Get_Stock_History(Stock=index, On_Date=S_Date)
                except Exception as err:
                    Critical(err)
                    Critical("{} has no Close price on this date".format(index))
                    continue
                try :
                    F_Stock_Price = F_Stock_Price[0][index]['Close']
                    S_Stock_Price = S_Stock_Price[0][index]['Close']

                except Exception as err:
                    Critical(err)
                    Critical("{} has no Close price on Date ".format(index))
                    continue
                Pchg = ((S_Stock_Price - F_Stock_Price)/F_Stock_Price) * 100

                Info("  F_Year : {} \n\
                        S_Year : {} \n\
                        New_Attr : {} \n\
                        F_Date : {} F_Stock_Price : {}\n\
                        S_Date : {} S_Stock_Price : {} \n\
                        ".format(  F_Year,
                                S_Year,
                                New_Attr,
                                F_Date,
                                F_Stock_Price,
                                S_Date,
                                S_Stock_Price,
                              ))
                BalanceSheet_Param_PChg_Df = BalanceSheet_Param_PChg_Df.set_value(index=index,col=New_Attr, value=Pchg)

        return BalanceSheet_Param_PChg_Df

    def Make_Columns_with_Qly_and_Req_Cols(self, Qlys):

        Req_Cols_Dict = {}
        for Qly in Qlys:
            for Col in Req_Qly_Cols:
                Req_Cols_Dict[Qly+"."+Col] = 1
        return Req_Cols_Dict # {"Mar_18.PAT":1 , "Dec_17.PAT":1, "Sep_17.PAT":1, "Jun_17.PAT":1}

    def Get_Qly_Data_For_Linear_Regression(self):

        dh = Date_Helpers()
        Final_Qly_DF = pd.DataFrame()
        All_Stocks_Qly = list(FindData().Get_Qly_Details)
        Qlys = [] #Getting Quarter Months from DB result [u'Jun_17', u'Jun_16', u'Sep_16', u'Sep_17', u'Jun_18'] excluding "_id"
        for stock in All_Stocks_Qly:
            Qlys = []; Stock = stock["_id"]
            tmp_df = pd.DataFrame()
            Critical(Stock)
            Qlys = [Q for Q in stock.keys() if Q != "_id"]
            Qlys = list(set(Qlys)) # Making the list unique
            # Critical(Qlys)

            Ord_Qlys , Ord_Qlys_alias = dh.Qly_Increasing_Order(Qlys=Qlys)
            Req_Cols_Dict = self.Make_Columns_with_Qly_and_Req_Cols(Qlys)

            Req_Cols = list(FindData().Get_Qly_For_Cols(Stock_Id =Stock,  Cols=Req_Cols_Dict)) # limit avaialble
            df = self.Make_BalanceSheet_Dataframe(BalanceSheet_Detail_For_All_Stock=Req_Cols)

            New_Cols = {}
            for Old in df.columns:
                New = Ord_Qlys_alias[Old[:6]] + Old[6:]
                New_Cols[Old] = New
        # print(New_Cols)
            df.rename(New_Cols, axis=1, inplace=True)
            Final_Qly_DF = Final_Qly_DF.append(df)
        # print(df)
        return Final_Qly_DF


        # BalanceSheet_df = self.Make_BalanceSheet_Dataframe(BalanceSheet_Details_From_DB)

    def Qly_Param_Pchg(self, Qly_Df=None):
        Final = pd.DataFrame()
        for index in Qly_Df.index:
            tmp_df = pd.DataFrame()
            New_DF = pd.DataFrame()  # Create New BalaceSheet Df for each Stock
            All_Quarter_And_Values = []  # ['Mar_16_Net_Worth', 'Mar_17_Net_Worth', etc...]
            for column in Qly_Df.columns:
                All_Quarter_And_Values.append(column)

            Sorted_Quarters = sorted(set([q[:4] for q in sorted(All_Quarter_And_Values)]))  # ['Mar_16', Mar_17, ...]
            for i in range(len(Sorted_Quarters) - 1):
                Quarter = Sorted_Quarters[i][:2]  # Mar_
                L_Year = Sorted_Quarters[i][3:4]  # 16
                H_Year = Sorted_Quarters[i + 1][3:4]  # 17
                for attr in Req_Qly_Cols:
                    New_attr = Quarter + "_" + L_Year + "_" + H_Year + "_" + attr + "_PChg"  # Mar_16_17_Net_Worth_Pchg
                    L_Column = Quarter + "_" + L_Year + "_" + attr  # Mar_16_Net_Worth
                    H_Column = Quarter + "_" + H_Year + "_" + attr  # Mar_17_Net_Worth
                    # print (New_attr , L_Column, H_Column) #(u'RQ_1_2_PAT_PChg', u'RQ_1_PAT', u'RQ_2_PAT')
                    try:
                        Pchg = ((Qly_Df[L_Column] - Qly_Df[H_Column]) / Qly_Df[H_Column]) * 100
                        New_DF[New_attr] = Pchg
                    except KeyError:
                        Critical("{} does not have this key...".format(index))
                        continue
            Info("calculated for {}".format(index))
            Final = tmp_df.append(New_DF)  # This is done bcoz we need a New_DF created for Each Stock
        return Final

if __name__ == "__main__":

    # CSV_PATH_ORG = "C:/Users/nandpara/PycharmProjects/Machine_Learning1\Stock_Analysis_BalanceSheet.csv"
    CSV_PATH = os.path.join(os.path.dirname(__file__) + '_BalanceSheet_Param_PChg.csv')
    # Price_CHG_CSV_PATH = os.path.join(os.path.dirname(__file__) + 'Price_CHG.csv')
    # Qly_CSV_PATH = os.path.join(os.path.dirname(__file__) + 'Qly_Details.csv')
    Qly_CSV_PATH = os.path.join(os.path.dirname(__file__) + 'Qly_Details1.csv')
    Obj = Linear_Regression()
    df = Obj.Get_Qly_Data_For_Linear_Regression()
    df = Obj.Qly_Param_Pchg(Qly_Df=df)
    print (df)

    # df = Obj.Get_BalanceSheet_Data_For_Linear_Regression(from_csv=True)
    # Critical("Indexes in Main Balance Sheet df : {}".format(df.index))
    # df = Obj.Yearly_BalanceSheet_Param_Change_Percent(df)
    # df = Obj.Yearly_Stock_Price_Change_Percent(df)
    # print ("Showing Yearly_BalanceSheet_Param_Change_Percent Detaails...")
    # print (df)
    # for col in df.columns:
    #     print (col ,"*******", df[col])
    #
    # for index in df.index:
    #     print ("Indexes : {}".format(index))
    # print (df[['Mar_13_14_Secured_Loan_PChg']])
    # df = Obj.Yearly_Stock_Price_Change_Percent(df)
    df.to_csv(path_or_buf=Qly_CSV_PATH, index=True)
    # print (df[['Mar_14_Share_Capital','Mar_15_Share_Capital','Mar_16_Share_Capital','Mar_17_Share_Capital','Mar_18_Share_Capital']])
    # for cosnt (new_df[column])
    # from Pandas_Practice.Pandas_Helpers import Df_view
    # Df_view(df = df, Show_Full_Info= True)
    # Obj.Test()
    # for col in df.columns:
    #     print (col ,"*******", df[col])


"""
Each_Stock_BalanceSheet_Data
{u'Mar_16': {u'Share_Capital': 776.28, u'Misc_Expenses': 0.0, u'Net_Current_Assessts': 1611700.9, u'Sundry_Debtors': 0.0, 
u'Total_Liabilities': 2099187.46, u'Capital_Work_In_Progress': 570.12, u'Provisions': 0.0,
 u'Loans_And_Advances': 1604108.82, u'Investments': 477097.28, u'Unsecured_Loan': 1730722.44, 
 u'Net_Worth': 144274.44, u'Reserves_Surplus': 143498.16, u'Gross_Block': 9819.16,
  u'Current_Liabilities': 159875.57, u'Total_Assests': 2099187.46, u'Net_Block': 9819.16, u'Depreciation': 0.0,
   u'Secured_Loan': 224190.59, u'Cash_and_Bank': 167467.66, u'Total_Current Liabilities': 159875.57, 
   u'Total_Current_Assets': 1771576.48, u'Inventories': 0.0}, u'Mar_17': {u'Share_Capital': 797.35,
    u'Misc_Expenses': 0.0, u'Net_Current_Assessts': 1741822.57, u'Sundry_Debtors': 0.0, u'Total_Liabilities': 2550731.12,
     u'Capital_Work_In_Progress': 573.93, u'Provisions': 0.0, u'Loans_And_Advances': 1725086.11,
      u'Investments': 765989.63, u'Unsecured_Loan': 2044751.39, u'Net_Worth': 188286.06, u'Reserves_Surplus': 155903.06,
       u'Gross_Block': 42344.99, u'Current_Liabilities': 155235.19, u'Total_Assests': 2550731.12, u'Net_Block': 10759.34,
        u'Depreciation': 0.0, u'Secured_Loan': 317693.66, u'Cash_and_Bank': 171971.65,
         u'Total_Current Liabilities': 155235.19, u'Total_Current_Assets': 1897057.76, u'Inventories': 0.0},
          u'Mar_14': {u'Share_Capital': 746.57, u'Misc_Expenses': 0.0, u'Net_Current_Assessts': 1289511.29,
           u'Sundry_Debtors': 0.0, u'Total_Liabilities': 1695821.64, u'Capital_Work_In_Progress': 0.0,
            u'Provisions': 0.0, u'Loans_And_Advances': 1253374.62, u'Investments': 398308.19, 
            u'Unsecured_Loan': 1394408.51, u'Net_Worth': 118282.25, u'Reserves_Surplus': 117535.68,
             u'Gross_Block': 8002.16, u'Current_Liabilities': 96412.96, u'Total_Assests': 1695821.64, u'Net_Block': 8002.16,
              u'Depreciation': 0.0, u'Secured_Loan': 183130.88, u'Cash_and_Bank': 132549.63, u'Total_Current Liabilities': 96412.96,
               u'Total_Current_Assets': 1385924.25, u'Inventories': 0.0}, u'Mar_15': {u'Share_Capital': 746.57, u'Misc_Expenses': 0.0,
                u'Net_Current_Assessts': 1406025.19, u'Sundry_Debtors': 0.0, u'Total_Liabilities': 1910381.75, 
                u'Capital_Work_In_Progress': 0.0, u'Provisions': 0.0, u'Loans_And_Advances': 1368861.94, u'Investments': 495027.4,
                 u'Unsecured_Loan': 1576793.24, u'Net_Worth': 128438.22, u'Reserves_Surplus': 127691.65, u'Gross_Block': 9329.16,
                  u'Current_Liabilities': 137698.05, u'Total_Assests': 1910381.75, u'Net_Block': 9329.16, u'Depreciation': 0.0,
                   u'Secured_Loan': 205150.29, u'Cash_and_Bank': 174861.3, u'Total_Current Liabilities': 137698.05,
                    u'Total_Current_Assets': 1543723.24, u'Inventories': 0.0}, 
                    u'Mar_18': {u'Share_Capital': 892.46, u'Misc_Expenses': 0.0, u'Net_Current_Assessts': 2186634.95, 
                    u'Sundry_Debtors': 0.0, u'Total_Liabilities': 3287613.92, u'Capital_Work_In_Progress': 791.54, u'Provisions': 0.0,
                     u'Loans_And_Advances': 2161874.39, u'Investments': 1060986.72, u'Unsecured_Loan': 2706343.29,
                     u'Net_Worth': 219128.56, u'Reserves_Surplus': 193388.11, u'Gross_Block': 39200.71, u'Current_Liabilities': 167138.08,
                      u'Total_Assests': 3312461.91, u'Net_Block': 39200.71, u'Depreciation': 0.0, u'Secured_Loan': 362142.07, u'Cash_and_Bank': 191898.64,
                       u'Total_Current Liabilities': 167138.08, u'Total_Current_Assets': 2353773.03, u'Inventories': 0.0}, u'_id': u'SBIN'}


    def Test(self):
        df = self.Get_BalanceSheet_Data_For_Linear_Regression()
        df['Net_Worth_Increase_Percentage'] = ((df['Mar_17_Net_Worth'] - df['Mar_16_Net_Worth']) / df['Mar_17_Net_Worth']) * 100
        print (df[['Net_Worth_Increase_Percentage']])
        Df_view(df, Show_Full_Info=True)
        print(df.loc[df['Net_Worth_Increase_Percentage']>10000, ['Net_Worth_Increase_Percentage']])
        # print(Filler)
        # print(df.iloc[0])
        # print(Filler)
        # print(df.loc['ZUARI'])
        df.loc[df['Net_Worth_Increase_Percentage']>100].hist()
        plt.show()

"""