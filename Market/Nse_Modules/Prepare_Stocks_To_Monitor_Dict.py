import pandas as pd
STOCKS_TO_MONTIOR={}

Required_Fields = ['SYMBOL', 'BUY', 'SELL', 'TOTTRDQTY']
df = pd.read_csv('20180508.csv', usecols=Required_Fields)
Total= len(df.index)
df = df.to_dict()

# print (type(df),df)

for symbol in df:
    for i in range(Total):
        SYMBOL = df['SYMBOL'][i]
        BUY = float(df['BUY'][i])
        SELL = float(df['SELL'][i])
        STOCKS_TO_MONTIOR[SYMBOL] = {'Buy':BUY, 'Sell':SELL, 'Popup_Shown_Already':False}


print (STOCKS_TO_MONTIOR)

