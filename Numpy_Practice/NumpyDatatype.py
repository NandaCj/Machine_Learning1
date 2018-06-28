import numpy as np

List = [1, 2, 3]
Dtype = np.dtype([('FirstValue', 'f4'), ('SecondValue', 'f4')])

Array = np.array([List, List, List], dtype=Dtype)
print (Array)
for i in Array:
    print("Each in Array", type(i), i)
    # for j in i:
    #     print("Each in Array", type(j), j)

"""
[[(1.,) (2.,) (3.,)]
 [(1.,) (2.,) (3.,)]
 [(1.,) (2.,) (3.,)]]
Each in Array <class 'numpy.void'> (1.,)
Each in Array <class 'numpy.void'> (2.,)
Each in Array <class 'numpy.void'> (3.,)
Each in Array <class 'numpy.void'> (1.,)
Each in Array <class 'numpy.void'> (2.,)
Each in Array <class 'numpy.void'> (3.,)
Each in Array <class 'numpy.void'> (1.,)
Each in Array <class 'numpy.void'> (2.,)
Each in Array <class 'numpy.void'> (3.,)
"""



# Array = np.array(List, dtype=Data)
# print(Array)
# student = np.dtype([('name','S20'), ('age', 'i1'), ('marks', 'f4')])
# print(student)

