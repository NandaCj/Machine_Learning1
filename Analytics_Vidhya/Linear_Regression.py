from sklearn import linear_model
from Helpers import Helpers
import numpy as np

class Linear_Regression:


    def __init__(self):
        pass
    
    def Sample_Dataset_For_Linear_Regression(self):
        Feature = np.array([x for x in range(1,100)][:10])
        Value = np.array([2*x for x in range(1,100) if x%2 == 0][:10])
        return Feature, Value
        
    def Predict_With_Linear_Regression(self, Feature, Value, Test=""):
        linear = linear_model.LinearRegression()
        # Value = Value.values.reshape(-1, 1)
        # Feature = Feature.values.reshape(-1, 1)
        # Test = Test.values.reshape(-1, 1)

        Value = Value.reshape(-1, 1)
        Feature = Feature.reshape(-1, 1)
        # Test = Test.reshape(-1, 1)

        print ("Fitting :",linear.fit(Feature, Value))
        print ("Score :",linear.score(Feature, Value))
        print('Coefficient: \n', linear.coef_)
        print('Intercept: \n', linear.intercept_)
        predicted = linear.predict(Test)
        print ("Predicted :",predicted)

if __name__ == "__main__":
    obj = Linear_Regression()
    Feature, Value =  obj.Sample_Dataset_For_Linear_Regression()
    Feature = np.array([1, 2, 3, 4, 5])
    Value = np.array([5, 6, 7, 8, 9])
    Helpers().Print_Type_And_Value(Feature, Value)
    obj.Predict_With_Linear_Regression(Feature, Value, 5)
    #obj.Predict_With_Linear_Regression()
