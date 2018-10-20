# Попытка решения задачи простым перебором
import numpy as np
import InitialConditions as ic
import Measures as criteria
from Permutations import Permutation

X_lkq = np.zeros((ic.L,ic.K,ic.Q))

J_max = 0
X_lkq_optimal = np.zeros((ic.L,ic.K,ic.Q))

for l in range(ic.L):
    for k in range(ic.K):
        for q in range(ic.Q):
            #формирование очередного вида матрицы
            for i in range(ic.A_ql[q,l]):
                #проверка выполнения ограничения по дальности
                if(criteria.checkDistances(l,q,k)):
                    X_lkq[l, k, q] = i
                else:
                    X_lkq[l, k, q] = 0
                #вычисление значения критерия
                J = criteria.J(X_lkq)
                if (J > J_max):
                    J_max = J
                    X_lkq_optimal = X_lkq
                else:
                    continue
print("Значение критерия J = %f. Оптимальная матрица целераспределения:" % J_max)

print(X_lkq_optimal)
for i in range(ic.Q):
    print("Аэродром № " + str(i))
    print(np.array(X_lkq_optimal[:,:,i]).transpose())
    print("\n")
