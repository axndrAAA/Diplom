# Попытка решения задачи простым перебором
import numpy as np
import InitialConditions as ic
import Measures as criteria
from Permutations import Permutation

def printmatrix(x_lkq):
    for i in range(ic.Q):
        print("Аэродром № " + str(i))
        print(np.array(x_lkq[:, :, i]).transpose())
        print("\n")

X_lkq = np.zeros((ic.L,ic.K,ic.Q))

J_max = -1000
X_lkq_optimal = np.zeros((ic.L,ic.K,ic.Q))

# Формируем возможные комбинации для каждого из аэродромов
lim = ic.Q
prmts_ql = []
for q in range(ic.Q):
    mq = []
    for l in range(ic.L):
        p = Permutation(ic.K,ic.A_ql[q,l])
        m = p.getAll()
        mq.append(m)
    prmts_ql.append(mq)

cnt = 0
# #для 3 типов 4 кластеров и одного аэродрома
for q in range(ic.Q):
    for l1 in range(len(prmts_ql[q][0])):
        X_lkq[0, :, q] = prmts_ql[q][0][l1]
        for l2 in range(len(prmts_ql[q][1])):
            X_lkq[1, :, q] = prmts_ql[q][1][l2]
            for l3 in range(len(prmts_ql[q][2])):
                X_lkq[2, :, q] = prmts_ql[q][2][l3]
                if cnt == 10456:
                    cnt = cnt
                cnt += 1
                # проверка выполнения ограничения по дальности
                if not criteria.checkDistances(X_lkq):
                    continue
                # вычисление значения критерия
                J = criteria.J(X_lkq)
                if J > J_max:
                    J_max = J
                    X_lkq_optimal = X_lkq.copy()
                else:
                    continue

print("Значение критерия J = %f. Оптимальная матрица целераспределения:" % J_max)

printmatrix(X_lkq_optimal)



