from sklearn import linear_model
from Helpers.Helpers import Helpers
# from sklearn.cross_validation import train_test_split
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
        # Helpers().Print_Type_And_Value(Feature, Value)
        print ("Fitting :",linear.fit(Feature, Value))
        print ("Score :",linear.score(Feature, Value))
        print('Coefficient: \n', linear.coef_)
        print('Intercept: \n', linear.intercept_)
        return linear

    def Linear_Fit_Feature_Value(self, Feature, Value):
        linear = linear_model.LinearRegression()
        linear.fit(Feature, Value)
        score = linear.score(Feature, Value)
        print ("Score/Accuracy  of this Linear Prediction... {}".format(score))
        print("linear.intercept_ : {}".format(linear.intercept_))
        print("linear.coef_ : {}".format(linear.coef_))
        return linear

    def Linear_Predict(self, linear, Predict_This):
        Predicted_Value = linear.predict(Predict_This)
        print("Predicted_Value",Predicted_Value)
        return Predicted_Value

    def RMSE(self, Actual_Values , Predicted_Values):
        from sklearn.metrics import mean_squared_error as mse
        Mse = mse(Actual_Values, Predicted_Values)
        RMSE = np.sqrt(Mse)
        print("Actual_Values :{}".format(Actual_Values))
        print("RMSE : {}".format(RMSE))
        return RMSE

if __name__ == "__main__":

    # Feature = np.array([[1, 2, 3, 4, 5],[1,2,3,4,5]])
    # Value = np.array([[5], [6]])
    Feature = np.array([[1], [2], [3], [4], [5]])
    Value = np.array([[10], [20], [30], [40], [50]])

    obj = Linear_Regression()
    linear = obj.Linear_Fit_Feature_Value(Feature, Value)
    Actual_Values = np.array([[110], [120], [130], [140], [145]])
    Predicted_values = obj.Linear_Predict(linear, np.array([[11], [12], [13], [14], [15]]))
    RMSE = obj.RMSE(Actual_Values, Predicted_values)
