# Попытка решения задачи простым перебором
import numpy as np
import InitialConditions as ic
from Permutations import Permutation
from OptimalDefinition import OptimalDefinition


def print_matrix(x_lkq):
    for i in range(ic.Q):
        print("Аэродром № " + str(i))
        print(np.array(x_lkq[:, :, i]).transpose())
        print("\n")


def l_boost(l, n, nl_indexes, prmts_ql, x_lkq, opt_def):
    #  условие выхода
    if nl_indexes[0] == len(prmts_ql[0][0]):
        return

    if l == ic.L - 1:
        #  дошли до края l измерения
        for nl_indexes[l] in range(len(prmts_ql[0][l])):
            X_lkq[l, :, 0] = prmts_ql[0][l][nl_indexes[l]]
            opt_def.checkMatrix(x_lkq)
        l -= 1
        l_boost(l, nl_indexes, prmts_ql, x_lkq, opt_def)
    else:
        if nl_indexes[l] < len(prmts_ql[0][l]):
            X_lkq[l, :, 0] = prmts_ql[0][l][nl_indexes[l]]
            nl_indexes[l] += 1
            l += 1
            l_boost(l, nl_indexes, prmts_ql, x_lkq, opt_def)
        else:
            nl_indexes[l] = 0
            l -= 1
            l_boost(l, nl_indexes, prmts_ql, x_lkq, opt_def)



X_lkq = np.zeros((ic.L, ic.K, ic.Q))

# Формируем возможные комбинации для каждого из аэродромов
lim = ic.Q
prmts_ql = []
max_prmts_count = 0
for q in range(1):  # debug:  ic.Q
    mq = []
    a = 1
    for l in range(ic.L):
        p = Permutation(ic.K, ic.A_ql[q, l])
        m = p.getAll()
        a *= len(m)
        mq.append(m)
    max_prmts_count += a
    prmts_ql.append(mq)

print('Макс. число перестановок: ' + str(max_prmts_count))

optDef = OptimalDefinition()  # объект содержащий оптимальное решение

nl_indexes = np.ones(ic.L, dtype=np.int)*-1
l_boost(0, nl_indexes, prmts_ql, X_lkq, optDef)

i = 1
# для 3 типов 4 кластеров и одного аэродрома
# for q in range(ic.Q):
# q = 0
# for l1 in range(len(prmts_ql[q][0])):
#     X_lkq[0, :, q] = prmts_ql[q][0][l1]
#     for l2 in range(len(prmts_ql[q][1])):
#         X_lkq[1, :, q] = prmts_ql[q][1][l2]
#         for l3 in range(len(prmts_ql[q][2])):
#             X_lkq[2, :, q] = prmts_ql[q][2][l3]
#             optDef.checkMatrix(X_lkq)



print("Значение критерия J = %f. Оптимальная матрица целераспределения:" % optDef.J_max)

print_matrix(optDef.X_lkq_optimal)



