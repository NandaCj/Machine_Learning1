import pandas as pd
from sklearn.model_selection import StratifiedShuffleSplit as strat

ipl_data = {'Team': ['Riders', 'Riders', 'Devils', 'Devils', 'Kings',
         'kings', 'Kings', 'Kings', 'Riders', 'Royals', 'Royals', 'Riders'],
         'Rank': [1, 2, 2, 3, 3,4 ,1 ,1,2 , 4,1,2],
         'Year': [2014,2015,2014,2015,2014,2015,2016,2017,2016,2014,2015,2017],
         'Points':[876,789,863,673,741,812,756,788,694,701,804,690]}

df = pd.DataFrame.from_dict(ipl_data)
df1 = pd.DataFrame(ipl_data)

print(df)

split = strat(n_splits=1, test_size=0.3, random_state=42)
splitted = split.split(X=df, y=df['Rank'])
print(type(splitted))
for i in splitted:
    for k in i:
        print(df.loc[k])


# print(type(train), type(test))

# Split returns a generator of Tuples of test and Train set indexes array