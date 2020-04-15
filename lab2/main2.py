import numpy as np
import nashpy as nash
import re
import matplotlib.pyplot as plt

n = 0
H = []
row_d = []
col_d = []
alpha = []
beta = []
for_I = []
for_J = []

with open('input2.txt', 'r+') as f:
    n = int(f.readline())
    for line in f.readlines():
        H.append([int(j) for j in line.split(' ')])

for i in range(n):
    alpha.append(min(H[i]))
a = max(alpha)

h = np.array(H)
for i in range(len(H[0])):
    beta.append(max(h[:, i]))
b = min(beta)

if a == b:
    print("Игра разрешима в чистых стратегиях.")
else:
    print("Игра не разрешима в чистых стратегиях.")

print("alpha =", a)
print("beta =", b)
H_np = np.array(H)
rps = nash.Game(H_np)
equilibria = rps.support_enumeration()
string = str(list(equilibria))
variance = re.findall(r'[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?', string)
p = variance[:n]
q = variance[n:(n + len(H[0]))]

for i in range(len(p)):
    if p[i] == '0.':
        row_d.append(i)
    else:
        for_I.append(int(i))
for j in range(len(q)):
    if q[j] == '0.':
        col_d.append(j)
    else:
        for_J.append(int(j))
row_d = row_d[::-1]
col_d = col_d[::-1]
for row in row_d:
    H_np = np.delete(H_np, row, axis=0)
for col in col_d:
    H_np = np.delete(H_np, col, axis=1)
I = 0.
H_np_trans = H_np.transpose()
for i in range(len(H_np_trans[0])):
    I = I + H_np_trans[0][i] * float(p[for_I[i]])
print("Значение игры I = ", I)
print("Оптимальная стратегия первого игрока:")
print("p =", p)
print("Оптимальная стратегия второго игрока:")
print("q =", q)
H_np_trans = H_np.transpose()
plt.plot([0, 1], [H_np[1][0], H_np[0][0]], [0, 1], [H_np[1][1], H_np[0][1]], 'r', 'b')
plt.xlim(0, 1)
plt.ylabel("Оптимальная стратегия 1-го игрока")
plt.xlabel("Значение игры")
plt.show()

plt.plot([0, 1], [H_np[0][1], H_np[0][0]], [0, 1], [H_np[1][1], H_np[1][0]], 'r', 'b')
plt.xlim(0, 1)
plt.xlabel("Значение игры")
plt.ylabel("Оптимальная стратегия 2-го игрока")
plt.show()
