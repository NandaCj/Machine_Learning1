import numpy as np

Array = np.array([[1,2,3,4],[4,3,2,1], [4,3,2,1], [4,3,2,1]])

print (Array.shape)

print (Array.reshape(4,4))

#print (Array.ndim)

print (Array[0].reshape(4,1))

print (Array.flags)