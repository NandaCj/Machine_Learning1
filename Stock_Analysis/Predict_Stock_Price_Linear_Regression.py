from sklearn import linear_model
import pandas as pd
import numpy as np
from Helpers.Logging import *
from Helpers.Helpers import Helpers
from Data.From_Db import FindData
import matplotlib.pyplot as plt
from Pandas_Practice.Pandas_Helpers import Df_view
from Data.ET.Common_Data import BalanceSheet_March_Dict, BalanceSheet_Param_Dict
import os, re
from datetime import datetime
from pandas.tseries.offsets import BMonthEnd
Filler = "****************************************************************"
class Linear_Regression:

    def __init__(self):
        pass

    def Add_BalanceSheet_Data_To_Dataframe(self, Complete_Balace_Sheet_Data):
        Info(Filler)
        UnUsual_Stock = []
        Stock = ""
        BalanceSheet_Dict = {}
        df_Columns = []
        BalanceSheet_df = None
        for Each_Stock_BalanceSheet_Data in Complete_Balace_Sheet_Data:
            try:
                Stock = str(Each_Stock_BalanceSheet_Data["_id"])  # HDFC
                Info("Stock : {}".format(Stock))
                BalanceSheet_Dict[Stock] = {}
                # Critical(type(Each_Stock_BalanceSheet_Data))
                # Critical(Each_Stock_BalanceSheet_Data)
                for Each_March in Each_Stock_BalanceSheet_Data.keys():
                    #Critical("Each_March :{}".format(Each_March))
                    if Each_March == "_id":
                        continue
                    for Each_Attr in Each_Stock_BalanceSheet_Data[Each_March].keys():
                        BalanceSheet_Attr_Value = Each_Stock_BalanceSheet_Data[Each_March][Each_Attr]
                        Info("BalanceSheet_Attr_Value : {}".format(BalanceSheet_Attr_Value))
                        BalanceSheet_Attr = Each_March + "_" + Each_Attr # Mar_18_Net_Worth
                        Info("BalanceSheet_Attr : {}".format(BalanceSheet_Attr))
                        # BalanceSheet_Dict["_id"] = {Stock : {}}

                        BalanceSheet_Dict[Stock][BalanceSheet_Attr] = BalanceSheet_Attr_Value
                        Info("BalanceSheet_Dict : {}".format(BalanceSheet_Dict))
                        # BalanceSheet_Dict[Stock]
                        df_Columns.append(BalanceSheet_Attr)

            except Exception as err:
                Critical(err)
                UnUsual_Stock.append(Stock)
                Critical("Error in Adding {} BalanceSheet Details to Dataframe ...".format(Stock))
        BalanceSheet_df = pd.DataFrame.from_dict(BalanceSheet_Dict, orient="index")
        Info (BalanceSheet_Dict)
        Critical("Total {} Stocks Are UnUsual in having BalaceSheet Details ".format(len(UnUsual_Stock)))
        # Critical("List : {}".format(",".join(UnUsual_Stock)))
        Critical(UnUsual_Stock)
        return BalanceSheet_df


    def Get_BalanceSheet_Data_For_Linear_Regression(self, from_csv = False):
        if from_csv :
            BalanceSheet_df = pd.DataFrame.from_csv(path=CSV_PATH_ORG)
            return BalanceSheet_df
        BalanceSheet_Details_From_DB = list(FindData().Get_Balance_Sheet_Details)
        Info("BalanceSheet_Details_From_DB : \n {}".format(BalanceSheet_Details_From_DB))
        BalanceSheet_df = self.Add_BalanceSheet_Data_To_Dataframe(BalanceSheet_Details_From_DB)
        # Helpers().Pickle_Dump(BalanceSheet_df)
        # BalanceSheet_df = Helpers().Pickle_Load()

        # Df_view(BalanceSheet_df, Show_Full_Info=True)
        # print (BalanceSheet_df)
        # BalanceSheet_df.hist()
        # plt.show()

        return BalanceSheet_df



    def Yearly_BalanceSheet_Param_Change_Percent(self, DF=None):

        Final_DF = pd.DataFrame()
        for index in DF.index[:50]:
            New_DF = pd.DataFrame()
            Info("Finding Yearly_BalanceSheet_Param_Change_Percent for Stock :{} ".format(index))
            # df = df.iloc[num].dropna(axis='columns')
            try:
                df = DF.loc[[index]].dropna(axis='columns')
            except Exception as err:
                Critical(err)
                Critical("{} has issue in this Dataframe".format(index))
                continue
            Col = []

            for column in df.columns:
                Col.append(column)
            Sorted_List = sorted(set([q[:6] for q in sorted(Col)]))

            Col_Diff = []
            for i in range(len(Sorted_List) - 1):
                Mon = Sorted_List[i][:3]  # Mar_
                L_Year = Sorted_List[i][4:6]  # 15
                h = Sorted_List[i + 1]
                H_Year = h[4:6]
                for attr in BalanceSheet_Param_Dict.values():
                    New_attr = Mon + "_" + L_Year + "_" + H_Year + "_" + attr + "_PChg"
                    L_Column = Mon + "_" + L_Year + "_" + attr
                    H_Column = Mon + "_" + H_Year + "_" + attr
                    # print(L_Column , H_Column)
                    Col_Diff.append(New_attr)
                    # New_DF.append(df)
                    New_DF[New_attr] = ((df[H_Column] - df[L_Column]) / df[L_Column]) * 100
                    # print("New_DF...\n",New_DF)
            Final_DF = Final_DF.append(New_DF)
            # print("Final_DF \n", Final_DF)

            # Final_DF.append(New_DF)
            # print(New_DF['Mar_13_14_Secured_Loan_PChg'])
            # print(Final_DF)
            # for col in New_DF.columns:
            #     print (col, "*******", New_DF[col])
            #
            # for index in New_DF.index:
            #     print ("Indexes : {}".format(index))
        return Final_DF

    def Yearly_Stock_Price_Change_Percent(self, DF):
        for index in DF.index[:50]:
            try:
                df = DF.loc[[index]].dropna(axis='columns')
            except:
                Critical("{} has issue in this Dataframe".format(index))
                continue
            Col = []
            for column in df.columns:
                Col.append(column)
            Sorted_List = sorted(set([q[:9] for q in sorted(Col)])) # Mar_14_15
            Years = re.findall(r'\d+', " ".join(Sorted_List))
            Mon = Col[2][:3]
            print (Years)
            Sorted_Years = sorted(set(Years))
            for i in range(len(set(Years)) - 1):
                F_Year = '20'+Sorted_Years[i]
                S_Year = '20'+Sorted_Years[i+1]
                New_Attr = Mon +"_"+ Sorted_Years[i] +"_"+Sorted_Years[i+1]+"_Stock_Price_PChg"
                F_Date = datetime(int(F_Year), 1, 4)
                S_Date = datetime(int(S_Year), 1, 4)
                F_Date = BMonthEnd().rollforward(F_Date)
                S_Date = BMonthEnd().rollforward(S_Date)
                try:
                    F_Stock_Price = FindData().Get_Stock_History(Stock=index, On_Date=F_Date)
                    S_Stock_Price = FindData().Get_Stock_History(Stock=index, On_Date=S_Date)
                except Exception as err:
                    Critical(err)
                    Critical("{} has no Close price on this date".format(index))
                    continue
                Critical("F_Year :{}".format(F_Year))
                Critical("S_Year :{}".format(S_Year))
                Critical("F_Date:{}".format(F_Date))
                Critical("S_Date :{}".format(S_Date))
                Critical("F_Stock_Price: {}".format(F_Stock_Price))
                Critical("S_Stock_Price :{}".format(S_Stock_Price))
                try :
                    F_Stock_Price = F_Stock_Price[0][index]['Close']
                    S_Stock_Price = S_Stock_Price[0][index]['Close']
                except Exception as err:
                    Critical(err)
                    Critical("{} has no Close price on Date ".format(index))
                    continue
                print(F_Year , F_Stock_Price)
                print(S_Year, S_Stock_Price)
                Pchg = ((S_Stock_Price - F_Stock_Price)/F_Stock_Price) * 100
                print(New_Attr , Pchg)
                # df[New_Attr] = Pchg
                DF = DF.set_value(index=index,col=New_Attr, value=Pchg)
                # DF = DF.append(pd.DataFrame.from_dict({index:Pchg}, orient='index', columns=[New_Attr]), ignore_index=False)
                Critical("Index : {} PChg : {}".format(index,Pchg))
                print(DF[New_Attr])

        return DF



if __name__ == "__main__":

    CSV_PATH_ORG = "C:/Users/nandpara/PycharmProjects/Machine_Learning1\Stock_Analysis_BalanceSheet.csv"
    CSV_PATH = os.path.join(os.path.dirname(__file__) + '_BalanceSheet_Param_PChg.csv')
    Obj = Linear_Regression()
    df = Obj.Get_BalanceSheet_Data_For_Linear_Regression(from_csv=True)
    Critical("Indexes in Main Balance Sheet df : {}".format(df.index))
    df = Obj.Yearly_BalanceSheet_Param_Change_Percent(df)
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
    df.to_csv(path_or_buf=CSV_PATH, index=True)
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