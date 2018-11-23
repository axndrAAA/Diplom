# Попытка решения задачи простым перебором
from Permutations import Permutation
from OptimalDefinition import OptimalDefinition
from Plot import Plot
from datetime import datetime
from Measures import *

def print_matrix(x_lkq):
    for q in range(ic.Q):
        print("Аэр. " + str(q+1))
        for k in range(ic.K):
            for l in range(ic.L):
                print(str(x_lkq[q][l][k]) + ' ', end='')
            print()
        print()

# засекаем время
start_time = datetime.now()

# Формируем возможные комбинации для каждого из аэродромов
prmts_ql = []
max_prmts_count = 1
for q in range(ic.Q):
    mq = []
    a = 1
    for l in range(ic.L):
        p = Permutation(ic.K, ic.A_ql[q, l])
        m0 = p.getAll()
        m = checkDistanceConstraint(q, l, m0)
        a *= len(m)
        mq.append(m)
    max_prmts_count *= a
    prmts_ql.append(mq)

print('Макс. число перестановок: ' + str(max_prmts_count))

optDef = OptimalDefinition()  # объект содержащий оптимальное решение

# Собираем все возможные варианты матриц для каждого аэродрома
x_q = []
for q in range(ic.Q):
    # все возможные матрицы для данного аэродрома q
    x_matrixes = Permutation.permute(prmts_ql[q])

    # сохраняем
    x_q.append(x_matrixes)

# теперь перебираем матрицы аэродромов
matrixes = Permutation.permute(x_q)

plot = Plot()
plot.plotIC()

q=0

for x in matrixes:
    optDef.checkMatrix(x)

print("Значение критерия J = %f. Оптимальная матрица целераспределения:" % optDef.J_max)

print_matrix(optDef.X_lkq_optimal)

print('Затрачено времени: {}'.format(datetime.now() - start_time))

input("Press [enter] to continue.")


