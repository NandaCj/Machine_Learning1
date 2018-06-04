from recommendations import critics
from Helpers import Dict_Print
from math import sqrt
from Plot import Matplot
Dict_Print(critics)
Summary = """ 

Eucliean Distance score 
    gives distance between two points in two points in a graph 
    say if two points (x1, y1), (x2, y2) 
    formula :
         sqrt [(x1 - x2)^2 + (y1 - y2)^2]
         
"""

class Euclidean :
    def __init__(self):
        print (Summary)

    def Calculate_Distance(self, A , B): # A and B is tuple (x1, y1)
        print ("Finding Distance between {} and {}".format(A, B))

        x1, y1 = A; x2, y2 = B
        Distance = sqrt(pow(x1 - x2, 2) + pow(y1 - y2, 2))
        Score = 1/(1+Distance)

        print ("Euclidean Distance :", Distance)
        print ("Score :", Score)
        Matplot().Line_Plot("A Values", A, "B Values",B)
        # Matplot().Scatter_Plot("A Values", A, "B Values", B)

MovieA_Rating = [1]
MovieB_Rating = [1]
Euclidean().Calculate_Distance((1,2), (2,2))

MovieA = "You, Me and Dupree"
MovieB = "Snakes on a Plane"
for Critic, Ratings in critics.items():
    print (Critic)
    try:
        if MovieA in Ratings.keys():
            x1 = critics[Critic][MovieA]
            y1 = critics[Critic][MovieB]
            MovieA_Rating.append(x1)
            MovieB_Rating.append(y1)
    except:
        pass

print (MovieA_Rating, MovieB_Rating)
from matplotlib import pyplot as plt
plt.xlabel(MovieA); plt.ylabel(MovieB)
plt.scatter(MovieA_Rating, MovieB_Rating)#, (3.5, 3.5))
plt.show()




