# Попытка решения задачи простым перебором

import numpy as np
import BruteForce.InitialConditions as ic
import BruteForce.Measures as criteria

X_lkq = np.zeros((ic.L,ic.K,ic.Q))

J_max = 0
X_lkq_optimal = np.zeros((ic.L,ic.K,ic.Q))

for l in range(ic.L):
    for k in range(ic.K):
        for q in range(ic.Q):
            #формирование очередного вида матрицы
            for i in range(ic.A_ql[q,l]):
                X_lkq[l,k,q] = i
                #вычисление значения критерия
                J = criteria.J(X_lkq)
                if (J > J_max):
                    J = J_max
                    X_lkq_optimal = X_lkq
                else:
                    continue
print("Значение критерия J = %f. Оптимальная матрица целераспределения:" % J_max)

print(X_lkq_optimal)
