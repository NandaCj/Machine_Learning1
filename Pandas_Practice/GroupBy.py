import pandas as pd

ipl_data = {'Team': ['Riders', 'Riders', 'Devils', 'Devils', 'Kings',
         'kings', 'Kings', 'Kings', 'Riders', 'Royals', 'Royals', 'Riders'],
         'Rank': [1, 2, 2, 3, 3,4 ,1 ,1,2 , 4,1,2],
         'Year': [2014,2015,2014,2015,2014,2015,2016,2017,2016,2014,2015,2017],
         'Points':[876,789,863,673,741,812,756,788,694,701,804,690]}
df = pd.DataFrame(ipl_data)
grouped = df.groupby('Team')
#Grouped Returns <class 'pandas.core.groupby.groupby.DataFrameGroupBy'> which is iterable of Tuples
#Tuples has group name and That Group DataFrame
print(type(grouped))

for i in grouped:
    print(type(i), len(i))
    for k in i:
        print(type(k))
        print(k)

