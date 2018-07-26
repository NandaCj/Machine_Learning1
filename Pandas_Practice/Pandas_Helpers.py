import pandas as pd
from Helpers.Logging import Info
Filler = "***************************************************************************************************"
class Df_view:

    def __init__(self, df=None, Show_Full_Info=False):
        if Show_Full_Info:
            self.Head_df(df)
            self.Tail_df(df)
            self.Describe_Df(df)
            self.Info_Df(df)

    def Head_df(self, df):
        print("DataFrame Top 5 Data... \n ")
        print(df.head())
        print(Filler)

    def Tail_df(self, df):
        print("DataFrame Last 5 Data ... \n ")
        print(df.tail())
        print(Filler)

    def Describe_Df(self, df):
        print("DataFrame Description ... \n {}".format(df.describe()))
        print(Filler)

    def Info_Df(self, df):
        print("DataFrame Information .... \n {}".format(df.info()))
        print(Filler)


if __name__ == "__main__":
    Dict = {'SOLARINDS': 18.1, 'THEMISMED': 13.72, 'SALASAR': 9.96, 'ELAND': 47.99, 'MUKTAARTS': 11.29,
            'GESHIP': 150.78, 'KDDL': 13.43, 'ERIS': 13.75, 'UNIONBANK': 1228.44, 'MEGH': 25.43, 'GEECEE': 21.73,
            'SUPREMEINF': 41.98, 'MAANALU': 3.38, 'RECLTD': 1974.92, 'SORILINFRA': 30.57, 'UNIVCABLES': 34.7,
            'MERCATOR': 26.99, 'ESTER': 41.7, 'MINDAIND': 315.87, 'SUPREMEIND': 25.41, 'LAOPALA': 11.1}
    df = pd.DataFrame.from_dict(Dict, orient='index', columns=["Mar_17_Share_Capital"])
    Obj = Df_view(df=df, Show_Full_Info=True)
