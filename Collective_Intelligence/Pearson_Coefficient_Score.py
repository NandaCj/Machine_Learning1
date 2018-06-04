from recommendations import critics
from math import sqrt

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

Age_Income = {
                'City':{'Age':20 , 'Salary':8000, 'Age1':30 , 'Salary1':4500, 'Age2':40 , 'Salary2':6500, },
                'Village':{'Age':20 , 'Salary':8000*2, 'Age1':30 , 'Salary1':4500*2, 'Age2':40 , 'Salary2':6500*2, },
                'Nithya':{'Age':40 , 'Salary':40000},
                'Rasika':{'Age':50 , 'Salary':50000},
              }
# r = sim_pearson(critics, 'Gene Seymour', 'Toby')
r = sim_pearson(Age_Income, 'Village', 'Rasika')

print (r)

# 0.396059017191

