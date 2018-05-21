import numpy as np
List = [1, 2, 3]
Array = np.array([List, List, List, List])
print (type(Array),"\n", Array)

for i in Array:
    print ("Each in Array", type(i), i)


"""
Output 
<class 'numpy.ndarray'> 
 [[1 2 3]
 [1 2 3]
 [1 2 3]
 [1 2 3]]
Each in Array <class 'numpy.ndarray'> [1 2 3]
Each in Array <class 'numpy.ndarray'> [1 2 3]
Each in Array <class 'numpy.ndarray'> [1 2 3]
Each in Array <class 'numpy.ndarray'> [1 2 3]
Ou

"""