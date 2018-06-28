#Import Library of Gaussian Naive Bayes model
from sklearn.naive_bayes import GaussianNB
import numpy as np


"""
say here in X  1st value in array is number of good words
            2nd value is bad words
say in prediction Y the 1 means Good word
                        0 menas bad word 
      

"""
""" money terror betting god"""
#assigning predictor and target variables
x= np.array([[5,0,1,3],[4,3,1,2]])
Y= np.array([1, 0])
#Create a Gaussian Classifier
model = GaussianNB()

# Train the model using the training sets
model.fit(x, Y)

#Predict Output
predicted= model.predict([[3,0,3,1]])
print predicted