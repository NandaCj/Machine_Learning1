from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier as Tree_Class
from sklearn.tree import export_graphviz
import pandas as pd
import numpy as np
# iris = load_iris()
# print(type(iris))
# print(iris)

Dict = {'Ranjith':{'Age':28, 'salary':1000},
        'Ranjith1':{'Age':29, 'salary':2000},
        'Ranjith2':{'Age':30, 'salary':3000},
        'Ranjith3':{'Age':31, 'salary':4000},
        'Ranjith4':{'Age':32, 'salary':5000},
        'Ranjith5':{'Age':33, 'salary':6000},
        }

df = pd.DataFrame.from_dict(Dict, orient='index')
print(df)


Feature = np.array([[31],
                    [32],
                    [33],
                    [34],
                    [35],
                    [36],
                    ])
Value = np.array([[100], [100], [100], [400], [500], [600]])
# Feature = df['Age']
# Value = df['salary']
Tree_Class = Tree_Class(max_depth=2)
print(Tree_Class.fit(Feature, Value))
print(Tree_Class.predict([[33]]))



export_graphviz(Tree_Class, out_file='sample_decision_tree.dot', feature_names=['Age'], class_names='Salary', rounded=True,filled=True)
#http://webgraphviz.com/