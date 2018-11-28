from Market.Nse_Modules.Get_ET_Archieved_News import Get_ET_News
from Stock_News_Analysis.Clean_Data.Clean_Filtered_News import Clean_News_Data
from Stock_News_Analysis.Clean_Data.Make_News_To_Stock_Correlation import Map_News_To_Stock_Next_Day_Change
from Alogorithm_Implementation.Bayes import Bayes
from Helpers.Helpers import Print_Helpers
import pandas as pd
import os

BayesObj = Bayes()
Deco_Print = Print_Helpers().Decorate_And_Print
News = 'News'
Class = 'Class'
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

    def Train_MultiNB(self):
        News_Class = self.Prepare_New_Class_Dataframe()
        Vectorizer, Transformer, MultiNB_Predictor = BayesObj.Apply_MultinomialNB(News_Class[News], News_Class[Class])
        return Vectorizer, Transformer, MultiNB_Predictor

    def MultiNB_Predict(self, MultiNB_Predictor, Predict_This):
        Predicted = MultiNB_Predictor.predict(Predict_This)
        Deco_Print(Predicted)



if __name__ == "__main__":
    obj = Predict_News_Strength(Date='20181023')
    Vectorizer, Transformer, MultiNB_Predictor = obj.Train_MultiNB()
    Predict_This = ["crore profit rise r "]
    Predict_This = Vectorizer.transform(Predict_This)
    Predict_This = Transformer.transform(Predict_This)
    obj.MultiNB_Predict(MultiNB_Predictor, Predict_This=Predict_This)