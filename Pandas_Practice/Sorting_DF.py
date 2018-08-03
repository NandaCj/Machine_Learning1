import pandas as pd
# from Helpers.Logging import Info
Dict = {'SOLARINDS': 18.1, 'THEMISMED': 13.72, 'SALASAR': 9.96, 'ELAND': 47.99, 'MUKTAARTS': 11.29,
        'GESHIP': 150.78, 'KDDL': 13.43, 'ERIS': 13.75, 'UNIONBANK': 1228.44, 'MEGH': 25.43, 'GEECEE': 21.73,
        'SUPREMEINF': 41.98, 'MAANALU': 3.38, 'RECLTD': 1974.92, 'SORILINFRA': 30.57, 'UNIVCABLES': 34.7,
        'MERCATOR': 26.99, 'ESTER': 41.7, 'MINDAIND': 315.87, 'SUPREMEIND': 25.41, 'LAOPALA': 11.1}

df = pd.DataFrame.from_dict(Dict, orient='index', columns=['Mar_17_Net_Worth'])
class Sorting_DF:

    def __init__(self):
        pass

    def Sort_Df_By_Values(self, df, Col):
        """ Sorts the Df by the Specific Column"""
        print(df.sort_values(by=Col))

    def Sort_Df_By_Axis(self, df, Axis):
        """ Sorts DF Indexes i.e Columns """
        print(df.sort_index(axis=Axis, ascending=False))

if __name__ == "__main__":
    Obj = Sorting_DF()
    df['Mar_18_Net_Worth'] = 100
    Obj.Sort_Df_By_Axis(df=df, Axis=1)
    # Obj.Sort_Df_By_Values(df=df, Col=['Mar_17_Net_Worth'])
    # Obj.Sort_Df_By_Values(df=df, Col=['Mar_18_Net_Worth'])