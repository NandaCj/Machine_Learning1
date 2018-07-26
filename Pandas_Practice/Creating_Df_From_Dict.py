import pandas as pd
"""
To Treat Dict-Keys as the Index , pass Orient = "index"

"""
Dict = {'SOLARINDS': 18.1, 'THEMISMED': 13.72, 'SALASAR': 9.96, 'ELAND': 47.99, 'MUKTAARTS': 11.29,
        'GESHIP': 150.78, 'KDDL': 13.43, 'ERIS': 13.75, 'UNIONBANK': 1228.44, 'MEGH': 25.43, 'GEECEE': 21.73,
        'SUPREMEINF': 41.98, 'MAANALU': 3.38, 'RECLTD': 1974.92, 'SORILINFRA': 30.57, 'UNIVCABLES': 34.7,
        'MERCATOR': 26.99, 'ESTER': 41.7, 'MINDAIND': 315.87, 'SUPREMEIND': 25.41, 'LAOPALA': 11.1}

df = pd.DataFrame.from_dict(Dict, orient='index', columns=["Mar_17_Share_Capital"])

print (df)
print (df.info())
print (df.describe())