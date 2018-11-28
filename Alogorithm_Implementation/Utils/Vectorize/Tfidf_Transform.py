from sklearn.feature_extraction.text import TfidfTransformer
from Alogorithm_Implementation.Utils.Vectorize.Count_Vectorize import Count_Vecotorizer

Count_Vecotorizer_Obj = Count_Vecotorizer()
class Tfidf_Tranformer:

    def __init__(self):
        self.Tfidf_Transformer_Obj = TfidfTransformer()

    def Apply_Tfidf_Transform(self, Feature):
        Vectorizer , Counts = self.Get_Vectorizer_Count(Feature)
        self.Tfidf_Transformer_Obj.fit(Counts)
        Tfidf_Tranformered = self.Tfidf_Transformer_Obj.transform(Counts)
        print(Tfidf_Tranformered)
        return Vectorizer , self.Tfidf_Transformer_Obj, Tfidf_Tranformered

    def Get_Vectorizer_Count(self, Feature):
        Counter_Obj, Counts = Count_Vecotorizer_Obj.Apply_Count_Vecotorize(Feature=Feature)
        return Counter_Obj , Counts