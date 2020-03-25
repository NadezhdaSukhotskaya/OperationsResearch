from pulp import *

x1 = pulp.LpVariable("x1", lowBound=0)
x2 = pulp.LpVariable("x2", lowBound=0)
x3 = pulp.LpVariable("x3", lowBound=0)
x4 = pulp.LpVariable("x4", lowBound=0)
x5 = pulp.LpVariable("x5", lowBound=0)
problem = pulp.LpProblem('0',pulp.LpMaximize)
problem += 0.04*x1 + 0.06*x2 + 0.09* x3 + 0.075*x4 + 0.08*x5, "Функция цели"
problem += x4 + x5 >= 4.8,"1"
problem += -x1 - x2 + x3 >= 0, "2"
problem += 0.1*x1 + 0.07*x2+0.03*x3+0.05*x4+0.02*x5 <= 0.48, "3"
problem += x1+ x2+ x3 + x4 + x5 == 12, "4"
problem.solve()
print ("Результат:")
for variable in problem.variables():
    print (variable.name, "=", variable.varValue)
print ("Стоимость доставки:")
print (abs(value(problem.objective)))