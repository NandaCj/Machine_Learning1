from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import BernoulliNB
from sklearn.naive_bayes import GaussianNB
from Helpers.Helpers import Print_Helpers
from Alogorithm_Implementation.Utils.Vectorize.Tfidf_Transform import Tfidf_Tranformer

Tfidf_Tranformer_Obj = Tfidf_Tranformer()
Deco_Print = Print_Helpers().Decorate_And_Print
class Bayes:

    def __init__(self):
        self.MultinomialNB = MultinomialNB()
        self.BernoulliNB = BernoulliNB()
        self.GaussianNB = GaussianNB()

    def Apply_MultinomialNB(self, Feature, Value):
        """

        :param Feature: Pandas Dataframe Column
        :param Value: Pandas Dataframe Column
        :return: fitted MultinomialNB algorithm Object
        """
        Vectorizer, Transformer, Transformed = Tfidf_Tranformer_Obj.Apply_Tfidf_Transform(Feature)
        MultinomialNB_Fit = self.MultinomialNB.fit(Transformed, Value)

        return Vectorizer, Transformer, self.MultinomialNB

    def Predict_MultinomialNB(self, Predict_This):
        Predicted = self.MultinomialNB.predict(Predict_This)
        Deco_Print(Predicted)

