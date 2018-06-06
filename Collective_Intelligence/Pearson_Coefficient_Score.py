from recommendations import critics
from math import sqrt
from Helpers import Helpers
#https://github.com/nico/collectiveintelligence-book/blob/master/recommendations.py

def sim_pearson(prefs,p1,p2):
    # Get the list of mutually rated items

    si={}
    for item in prefs[p1]:
        if item in prefs[p2]:
            si[item]=1
    # Find the number of elements
    print (si)
    n=len(si)

    if n==0: # if they have no ratings in common, return 0
        return 0

    sum1=sum([prefs[p1][it] for it in si]) # Add up all the preferences
    sum2=sum([prefs[p2][it] for it in si])

    sum1Sq = sum([pow(prefs[p1][it], 2) for it in si])  # Sum up the squares
    sum2Sq = sum([pow(prefs[p2][it], 2) for it in si])

    pSum = sum([prefs[p1][it] * prefs[p2][it] for it in si]) # Sum up the products

    num = pSum - (sum1 * sum2 / n)
    den = sqrt((sum1Sq - pow(sum1, 2) / n) * (sum2Sq - pow(sum2, 2) / n))
    if den == 0:
        return 0
    r = num / den

    for i in si:
        print (prefs[p1][i] , prefs[p2][i])
    print (num , den)
    return r

from scipy.stats import pearsonr
#from Analytics_Vidhya.Linear_Regression import Linear_Regression

import numpy as np

def Pearsonr(x, y):
    Helpers().List_Print(x, y)
    R = pearsonr(x, y)
    print("Pearson R value:", R)
    return R


x = [1,2,3,4,5]
y = [12,96,-100,-500,111]
Feature = np.array(x)
Value = np.array(y)
Helpers().Print_Type_And_Value(Feature, Value)
Pearsonr(x, y)
Linear_Regression().Predict_With_Linear_Regression(Feature, Value, 5)


Age_Income = {
                'City':{'Age':20 , 'Salary':8000, 'Age1':30 , 'Salary1':4500, 'Age2':40 , 'Salary2':6500, },
                'Village':{'Age':20 , 'Salary':8000*2, 'Age1':30 , 'Salary1':4500*2, 'Age2':40 , 'Salary2':6500*2, },
                'Nithya':{'Age':40 , 'Salary':40000},
                'Rasika':{'Age':50 , 'Salary':50000},
              }
# r = sim_pearson(critics, 'Gene Seymour', 'Toby')
# r = sim_pearson(Age_Income, 'Village', 'Rasika')
# print (r)
