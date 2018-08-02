import pandas as pd
from Helpers.Logging import Info
Dict = {'SOLARINDS': 18.1, 'THEMISMED': 13.72, 'SALASAR': 9.96, 'ELAND': 47.99, 'MUKTAARTS': 11.29,
        'GESHIP': 150.78, 'KDDL': 13.43, 'ERIS': 13.75, 'UNIONBANK': 1228.44, 'MEGH': 25.43, 'GEECEE': 21.73,
        'SUPREMEINF': 41.98, 'MAANALU': 3.38, 'RECLTD': 1974.92, 'SORILINFRA': 30.57, 'UNIVCABLES': 34.7,
        'MERCATOR': 26.99, 'ESTER': 41.7, 'MINDAIND': 315.87, 'SUPREMEIND': 25.41, 'LAOPALA': 11.1}

# df = pd.DataFrame.from_dict(Dict, orient='index', columns=['Mar_Net_Worth'] )
df=pd.DataFrame()
df2 = pd.DataFrame.from_dict( {'Nandha': 99, 'Ranjith': 100}, orient='index', columns=['Age'])
print (df2)
df2['New']='Name'
print (df2)


