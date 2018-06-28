import numpy as np
List = [1, 'nandha', 3]
Array = np.array([List, List, List, List])
print (type(Array),"\n", Array)

for i in Array:
    print ("Each in Array", type(j), j)


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