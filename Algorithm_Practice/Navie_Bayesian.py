from sklearn.naive_bayes import GaussianNB
import numpy as np

x = np.array([
                ['Good', 'Good', 'Good'],
                ['Bad','Bad','Bad']
             ])

y = np.array(['GOOD', 'BAD'])

# model = GaussianNB()
# model.fit(x, y)

#predicted = model.predict(['Good', 'Good', 'Good'])
print (x)