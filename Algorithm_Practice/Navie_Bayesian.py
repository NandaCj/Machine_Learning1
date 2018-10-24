from sklearn.naive_bayes import GaussianNB,  MultinomialNB, BernoulliNB
import numpy as np

x = np.array([
                [1, 1, 1],
                [0,0,0],
                [2,2,2]
             ])

y = np.array(['GOOD', 'BAD', 'WORST'])
predict_this = [0,2,2]
#----------------------GaussianNB---------------
model = GaussianNB()
model.fit(x, y)

predicted = model.predict([predict_this])
print ("Gaussian Predict",predicted)


#----------------------MultinomialNB---------------
model = MultinomialNB()
model.fit(x, y)

predicted = model.predict([predict_this])
print ("MultinomialNB Predict",predicted)

#----------------------BaseNB---------------
model = BernoulliNB()
model.fit(x, y)

predicted = model.predict([predict_this])
print ("BernoulliNB Predict",predicted)
