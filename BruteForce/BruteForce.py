# Попытка решения задачи простым перебором

import numpy as np
import BruteForce.InitialConditions as ic

X_lkq = np.zeros(ic.L,ic.K,ic.Q)

for l in range(ic.L):
    for k in range(ic.K):
        for q in range(ic.Q):
            #формирование очередного вида матрицы
            for i in range(ic.A_ql[q,l]):
                X_lkq[l,k,q] = i
                #вычисление значения критерия