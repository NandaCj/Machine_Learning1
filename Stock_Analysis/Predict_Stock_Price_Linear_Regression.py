from sklearn import linear_model
import pandas as pd
import numpy as np
from Helpers.Logging import *
from Helpers.Helpers import Helpers
from Data.From_Db import FindData
import matplotlib.pyplot as plt
from Pandas_Practice.Pandas_Helpers import Df_view
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
                for Each_March in ["Mar_17", "Mar_16"]:
                    for Each_Attr in ["Reserves_Surplus", "Net_Worth"]:
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


    def Get_BalanceSheet_Data_For_Linear_Regression(self):

        # BalanceSheet_Details_From_DB = list(FindData().Get_Balance_Sheet_Details)
        # Info("BalanceSheet_Details_From_DB : \n {}".format(BalanceSheet_Details_From_DB))
        # BalanceSheet_df = self.Add_BalanceSheet_Data_To_Dataframe(BalanceSheet_Details_From_DB)
        # Helpers().Pickle_Dump(BalanceSheet_df)
        BalanceSheet_df = Helpers().Pickle_Load()

        # Df_view(BalanceSheet_df, Show_Full_Info=True)
        # print (BalanceSheet_df)
        # BalanceSheet_df.hist()
        # plt.show()
        return BalanceSheet_df

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


if __name__ == "__main__":
    Obj = Linear_Regression()
    # Obj.Get_BalanceSheet_Data_For_Linear_Regression()
    Obj.Test()



