import numpy as np

Array = np.arange(10, 100, 10)
print (Array)

print (Array[2:8])
print (Array[2:8:2])
print(Array[...,8])

Array = np.array([[10, 20, 30, 40, 50, 60, 70, 80, 90],[10, 20, 30, 40, 50, 60, 70, 80, 90]])

print (Array)
print (Array[1][2:8])

print(Array[...,8])
