from sklearn.feature_extraction.text import CountVectorizer
from Helpers.Helpers import Print_Helpers
Deco_Print = Print_Helpers().Decorate_And_Print

class Count_Vecotorizer:
    def __init__(self):
        self.Count_Vecotorizer_Obj = CountVectorizer()

    def Apply_Count_Vecotorize(self, Feature):
        """
        :param Feature: Pandas Dataframe Column
        :return:
        """
        print("Applying Vectorize...")
        self.Count_Vecotorizer_Obj.fit(Feature)
        Deco_Print(self.Count_Vecotorizer_Obj.get_feature_names())
        Counts = self.Count_Vecotorizer_Obj.transform(Feature)
        return self.Count_Vecotorizer_Obj, Counts



