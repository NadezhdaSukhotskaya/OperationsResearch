from scipy.optimize import linprog
import numpy as np

n = 0
H = []
alpha = []
beta = []

with open('input1.txt', 'r+') as f:
    n = int(f.readline())
    for line in f.readlines():
        H.append([int(j) for j in line.split(' ')])


for i in range(n):
    alpha.append(min(H[i]))
a = max(alpha)
h = np.array(H)
for i in range(len(H[0])):
    beta.append(max(h[:,i]))
b = min(beta)
if a == b:
    print("Игра разрешима в чистых стратегиях.\n")
else:
    print("Игра не разрешима в чистых стратегиях.\n")
x = [1 for i in range(n)]
a_ = np.array(H).transpose()*(-1)
b_ = [-1 for i in range(len(H[0]))]
print("Оптимальные решения: ")
x_solve = linprog(x, a_, b_).x
print ("x =", x_solve)
y = [-1 for i in range(len(H[0]))]
a_ub = H
b_ub = [1 for i in range(n)]#'1'
y_solve = linprog(y, a_, b_).x
print("y =", y_solve)
I = 1/sum(y_solve)
print ("\nЗначение игры  I = ", I)
print("\nОптимальные смешанные стратегии играков:")
p = [I*variable for variable in x_solve]
print("p =", p)
q = [I*variable for variable in y_solve]
print("q =", q)