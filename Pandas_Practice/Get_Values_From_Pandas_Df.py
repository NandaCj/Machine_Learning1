import pandas as pd
sales = [{'account': 'Jones LLC', 'Jan': 150, 'Feb': 200, 'Mar': 140},
         {'account': 'Alpha Co',  'Jan': 200, 'Feb': 210, 'Mar': 215},
         {'account': 'Blue Inc',  'Jan': 50,  'Feb': 90,  'Mar': 95 }]
df = pd.DataFrame(sales)

print (df)
Filler = "**********************"

class Get_Pandas_Df_Values :

    def Show_df_Index(self) :
        print(Filler)
        for index in df.index:
            print ("Indexes :",index)

    def Show_df_Columns(self):
        print(Filler)
        for row in df.columns:
            print(row)

    def Show_df_Rows(self):
        print(Filler)
        for row in df.iteritems():
            print(row)

    def Show_Rows_wrt_Index(self):
        print(Filler)
        for Row in df.loc[0]:
            print(Row)


if __name__ == "__main__":
    Obj = Get_Pandas_Df_Values()
    Obj.Show_df_Index()
    Obj.Show_df_Columns()
    Obj.Show_df_Rows()
    Obj.Show_Rows_wrt_Index()