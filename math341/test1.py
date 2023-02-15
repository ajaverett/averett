import numpy as np
import sympy as sp
from sympy import *

init_printing()


A = Matrix(np.array([
    [1,2,3],
    [4,5,6],
    [7,8,9]]))

B = Matrix(np.array([
    [10,11,12],
    [13,14,15],
    [16,17,18]]))


A.T+B.T == (A+B).T

A.T.T == A

(A*B).T == B.T*A.T

A = Matrix(np.array([
    [1,1,1],
    [1,2,3],
    [1,4,5]]))

B = Matrix(np.array([
    [2,0,0],
    [0,3,0],
    [0,0,5]]))

A*B == B*A

(A*B).T == A.T*B.T

(A+B).T == A.T+B.T


A = Matrix(np.array([
    [0,4,5,6],
    [-2,0,2,-8],
    [3,-1,4,0],
    [0,0,3,2]
    ]))

A.det()