import numpy as np
import sympy as sp
from sympy import init_printing, Matrix 
init_printing() #Will output latex looking results

# Question 1

A = Matrix([
    [1,1,0,1,-1,-1,1],
    [0,1,-1,1,-1,0,0],
    [-1,0,1,1,-1,1,-1],
    [0,-1,1,1,-1,-1,-1],
    [1,1,0,0,0,-1,1],
    [1,1,-1,0,-1,-1,-1]])

print(A.rref())

# [
# [1, 0, 0, 0, 0, 0, 2],
# [0, 1, 0, 0, 0, 0, 0],
# [0, 0, 1, 0, 0, 0, 0],
# [0, 0, 0, 1, 0, 0, 2],
# [0, 0, 0, 0, 1, 0, 2],
# [0, 0, 0, 0, 0, 1, 1]]

# Question 2

# Pivot Columns: 0, 1, 2, 3, 4, 5


# Question 3

# Assuming that A is a coefficient matrix, this means that A has 7 vectors with 6 entries per vector. According to Theorem 8, If a set contains more vectors than there are entries in a vector, this means that if A is consistent, it is linearly dependent

# Question 4

# Below is Matrix A where column: 'a_5' is the right side of an augmented matrix

# A_4rref = A[:, [0,1,2,3,4,6,5]].rref()[0]

# Take out columns
fifth_column = A[:,4]
other_columns = Matrix(np.delete(A, 4, axis=1))

other_columns = np.array(other_columns, dtype=float)
fifth_column = np.array(fifth_column, dtype=float)
x1 = Matrix(np.linalg.solve(other_columns, fifth_column))
A_4 = Matrix(np.append(other_columns, fifth_column, axis = 1))
A_4rref= A_4.rref()[0]
x = A_4rref[:,-1]
other_columns*x


# b = A_4rref[:,-1]

# add = Matrix(np.zeros((7,1)))


# for i in range(A_4rref.shape[1]-1):
#     add += (b[i]*A_4[i,:]).T


# other_columns = np.array(other_columns, dtype=float)
# fifth_column = np.array(fifth_column, dtype=float)


# float(x[-1])


# for i in range(5):
#     add += (float(x[i])*A_4[i,:]).T

