import pandas as pd
from Helpers.Logging import Info
Dict = {'SOLARINDS': 18.1, 'THEMISMED': 13.72, 'SALASAR': 9.96, 'ELAND': 47.99, 'MUKTAARTS': 11.29,
        'GESHIP': 150.78, 'KDDL': 13.43, 'ERIS': 13.75, 'UNIONBANK': 1228.44, 'MEGH': 25.43, 'GEECEE': 21.73,
        'SUPREMEINF': 41.98, 'MAANALU': 3.38, 'RECLTD': 1974.92, 'SORILINFRA': 30.57, 'UNIVCABLES': 34.7,
        'MERCATOR': 26.99, 'ESTER': '', 'MINDAIND': 315.87, 'SUPREMEIND': 25.41, 'LAOPALA': 11.1}
def show_isnull(df):
    print(df)
    print(df.isna())
    # print(df[df.isnull()== False])
    # print(df[df.isnull()== True])

df = pd.DataFrame.from_dict(Dict, orient='index', columns=['PAT'])
print(df.loc[df['PAT'] == 26.99])
# show_isnull(df)


# df = NQSheet[NQSheet.isnull().any(axis=1)]
