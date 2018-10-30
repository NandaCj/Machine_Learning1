from Market.Nse_Modules.Get_ET_Archieved_News import Get_ET_News
from Stock_News_Analysis.Clean_Data.Clean_Filtered_News import Clean_News_Data
from Stock_News_Analysis.Clean_Data.Make_News_To_Stock_Correlation import Map_News_To_Stock_Next_Day_Change
import pandas as pd
import os
from sklearn.naive_bayes import BernoulliNB, MultinomialNB

MultiNB = MultinomialNB()
Bernoulli = BernoulliNB()

class Predict_News_Strength():

    def __init__(self,
                Get_News=None,
                Clean_News=None,
                Map_News=None,
                Date =None):
        if Get_News:
            print("Getting News...")
            Get_ET_News(Date)
        if Clean_News:
            print("Cleaning News...")
            Clean_News_Data(Date)
        if Map_News:
            print("Mapping News...")
            Map_News_To_Stock_Next_Day_Change(Date)
        self.Date = Date

    def Prepare_New_Class_Dataframe(self):
        News_File = self.Date + "_News_Class_File.csv"
        News_File = os.path.dirname(__file__) + "/Clean_Data/Cleaned_Files/" + News_File
        print(News_File)
        News_Class_Df = pd.read_csv(News_File)
        print(News_Class_Df[['News', 'Class']])
        return News_Class_Df

    def Train_Bayes_Model(self):
        from sklearn.preprocessing import OneHotEncoder
        from sklearn.preprocessing import LabelEncoder
        le = LabelEncoder()
        encoder = OneHotEncoder()
        News_Class_Df = self.Prepare_New_Class_Dataframe()

        # # le.fit(News_Class_Df['News'])
        # News_Class_Df = News_Class_Df['News'].apply(le.fit_transform)
        # print(News_Class_Df)

        News_Class_Df = News_Class_Df[:-5].apply(le.fit_transform)
        print(News_Class_Df[-5:])
        MultiNB.fit(X=News_Class_Df['News'].values.reshape(-1,1), y=News_Class_Df['Class'])
        print(News_Class_Df['News'].values.reshape(-1,1))
        print(MultiNB.predict(News_Class_Df['News'].values.reshape(-1,1)))
obj = Predict_News_Strength(Date='20181023')
obj.Train_Bayes_Model()