import pandas as pd
from Helpers.Logging import Info
Dict = {'SOLARINDS': 18.1, 'THEMISMED': 13.72, 'SALASAR': 9.96, 'ELAND': 47.99, 'MUKTAARTS': 11.29,
        'GESHIP': 150.78, 'KDDL': 13.43, 'ERIS': 13.75, 'UNIONBANK': 1228.44, 'MEGH': 25.43, 'GEECEE': 21.73,
        'SUPREMEINF': 41.98, 'MAANALU': 3.38, 'RECLTD': 1974.92, 'SORILINFRA': 30.57, 'UNIVCABLES': 34.7,
        'MERCATOR': 26.99, 'ESTER': 41.7, 'MINDAIND': 315.87, 'SUPREMEIND': 25.41, 'LAOPALA': 11.1}

df = pd.DataFrame.from_dict(Dict, orient='index', columns=['Mar_Net_Worth'] )

# Info (df)
Filler = "**********************"

class Get_Pandas_Df_Values :

    def Show_df_Index(self) :
        Info(Filler)
        for index in df.index:
            Info ("Indexes :{}".format(index))

    def Show_df_Columns(self):
        Info(Filler)
        for row in df.columns:
            Info(row)

    def Show_df_Rows(self):
        Info(Filler)
        for row in df.iteritems():
            Info(row)

    def Show_Rows_wrt_Index_Number(self):
        Info(Filler)
        for i in range(len(df.index)):
            print(df.iloc[i]['Mar_Net_Worth'])

    def Show_Rows_wrt_Index_Value(self):
        Info(Filler)
        Info("\n {}".format(df.loc[['SALASAR']]))





if __name__ == "__main__":
    Obj = Get_Pandas_Df_Values()
    # Obj.Show_df_Index()
    # Obj.Show_df_Columns()
    # Obj.Show_df_Rows()
    # Obj.Show_Rows_wrt_Index_Number()
    Obj.Show_Rows_wrt_Index_Value()