import numpy as np
Array = np.array([[10, 20, 30, 40, 50, 60, 70, 80, 90],[100, 200, 300, 400, 500, 600, 700, 800, 900],
                  [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000]])


print (Array[[1],[3]])

# For Column Filtering
print (Array[1:3,[1,2,2,5]])

