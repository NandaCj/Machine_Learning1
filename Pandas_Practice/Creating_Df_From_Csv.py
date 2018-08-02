import os
import pandas as pd
from pandas.tseries.offsets import BMonthEnd
from datetime import datetime
from Data.ET.Common_Data import BalanceSheet_Param_Dict

CSV_File = os.path.join(os.path.dirname(os.path.dirname(__file__)) , 'Stock_Analysis_BalanceSheet.csv')
# C:\Users\nandpara\PycharmProjects\Machine_Learning1\Stock_Analysis_BalanceSheet.csv
print (CSV_File)

df = pd.DataFrame.from_csv(path = CSV_File)
Col = [] # Columns only available for That Stock
df = df.loc[['HDFC']].dropna(axis='columns')
# print (df)
for column in df.columns:
    Col.append(column)

New_DF = pd.DataFrame()
# print (Col)
Sorted_List = sorted(set([q[:6] for q in sorted(Col)]))
print (Sorted_List)
Col_Diff = []
for i in range(len(Sorted_List)-1):
    Mon = Sorted_List[i][:3] # Mar_
    L_Year = Sorted_List[i][4:6] #15
    h = Sorted_List[i+1]
    H_Year = h[4:6]
    for attr in BalanceSheet_Param_Dict.values():
        New_attr = Mon+"_"+L_Year+"_"+H_Year+"_"+attr+"_PChg"
        L_Column = Mon+"_"+L_Year+"_"+attr
        H_Column = Mon+"_"+H_Year+"_"+attr
        # print(L_Column , H_Column)
        Col_Diff.append(New_attr)
        df[New_attr] = ((df[H_Column] - df[L_Column])/df[L_Column]) * 100
    continue

# for j in Col_Diff:
#     print(j)

# for i in df[['Mar_14_Share_Capital','Mar_15_Share_Capital', 'Mar_14_15_Share_Capital_PChg']]:
#     print(i)
print(df['Mar_14_Share_Capital'])
print(df['Mar_15_Share_Capital'])
print(df['Mar_14_15_Share_Capital_PChg'])

for j in df.columns:
    print(j)

# dt = datetime(2017, 9, 12)
# offset = BMonthEnd()
# T = offset.rollforward(dt)
# print(type(T), T)