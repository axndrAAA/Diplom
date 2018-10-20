# Попытка решения задачи простым перебором
import numpy as np
import InitialConditions as ic
import Measures as criteria
from Permutations import Permutation

X_lkq = np.zeros((ic.L,ic.K,ic.Q))

J_max = 0
X_lkq_optimal = np.zeros((ic.L,ic.K,ic.Q))

# Формируем возможные комбинации для каждого из аэродромов
prmts_ql = []
for q in range(ic.Q):
    mq = []
    for l in range(ic.L):
        p = Permutation(ic.K,ic.A_ql[q,l])
        m = p.getAll()
        mq.append(m)
    prmts_ql.append(mq)


#для 3 типов 4 кластеров и одного аэродрома
    for l1 in range(len(prmts_ql[1])):
        X_lkq[1, :, 1] = prmts_ql[1, l1]
        for l2 in range(len(prmts_ql[2])):
            X_lkq[2, :, 1] = prmts_ql[2, l2]
            for l3 in range(len(prmts_ql[3])):
                X_lkq[3, :, 1] = prmts_ql[3, l3]

# попытка автоматизировать перебор по типам
# lx = np.zeros([ic.L])
# for l in range(ic.L):
#     for lx[l] in range(len(prmts[l])):
#         X_lkq[l, :, 1] = prmts[1, lx[l]]
#         for lx[2] in range(len(prmts[2])):
#             X_lkq[2, :, 1] = prmts[2, lx[2]]
#             for lx[3] in range(len(prmts[3])):
#                 X_lkq[3, :, 1] = prmts[3, lx[3]]

# for l in range(ic.L):
#     for k in range(ic.K):
#         for q in range(ic.Q):
#             #формирование очередного вида матрицы
#             for i in range(ic.A_ql[q,l]):
#                 #проверка выполнения ограничения по дальности
#                 if(criteria.checkDistances(l,q,k)):
#                     X_lkq[l, k, q] = i
#                 else:
#                     X_lkq[l, k, q] = 0
#                 #вычисление значения критерия
#                 J = criteria.J(X_lkq)
#                 if (J > J_max):
#                     J_max = J
#                     X_lkq_optimal = X_lkq
#                 else:
#                     continue
print("Значение критерия J = %f. Оптимальная матрица целераспределения:" % J_max)

print(X_lkq_optimal)
for i in range(ic.Q):
    print("Аэродром № " + str(i))
    print(np.array(X_lkq_optimal[:,:,i]).transpose())
    print("\n")
