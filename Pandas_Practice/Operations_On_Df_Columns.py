import pandas as pd


Dict = {"Value1":{"Mark":90, "Mark1":80, "Age":26}, "Value2":{"Mark":90, "Mark1":80, "Age":26}, "Value3":{"Mark":90, "Mark1":80, "Age":26},
        "Value4":{"Mark":90, "Mark1":0, "Age":26}, "Value5":{"Mark":90, "Mark1":80, "Age":26}, "Value6":{"Mark":90, "Mark1":80, "Age":26}}
df = pd.DataFrame.from_dict(Dict,  orient='index')

print(df['Mark'], df['Mark1'])
print((df['Mark'] + df['Mark1'])/ 2)
df['Avg_Mark'] = ((df['Mark'] - df['Mark1']) / df['Mark']) * 2

print(df['Mark1'] > 10)

# from Helpers.Helpers import Helpers
#
# df = Helpers().Pickle_Load()
#
# print df