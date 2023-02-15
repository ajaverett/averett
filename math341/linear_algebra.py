import numpy as np
import sympy as sp

from sympy import Eq, solve_linear_system, Matrix
from numpy import linalg

eq_1 = sp.Function('eq1') 
eq_2= sp.Function('eq2') 

x, y = sp.symbols("x y")

eq1 = Eq(2*x-y,-4)
eq2 = Eq(3*x-y,-2)

display(eq1, eq2)

row1 = [2,-1,-4]
row2 = [3,-1,-2]

system = Matrix((row1,row2))

solve_linear_system(system,x,y)

nrow1 = [2,-1]
nrow2 = [3,-1]

nmat = np.array([nrow1, nrow2])

cons = ([-4,-2])

answer = linalg.solve(nmat, cons)








x, y = sp.symbols('x y')

system = [
sp.Eq(4*x + 7*y, -9),
sp.Eq(5*x + 8*y, -10)
]

sp.linsolve(system,x,y)

system.rref()



M = sp.Matrix([
    [1,2],
    [3,1]
])

display(M.rref())