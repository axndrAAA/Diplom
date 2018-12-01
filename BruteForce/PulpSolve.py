from pulp import *
import numpy as np
import InitialConditions1 as ic
import  Measures as measures


# LP task
problem = LpProblem("UAV scheduling problem", LpMinimize)

# max val in matrix
N = ic.A_ql.max()

# positions = [(q, l, k) for q in range(ic.Q) for l in range(ic.L) for k in range(ic.K)]

# Determine variable as binary matrix
v = LpVariable.dicts("vals", (range(ic.Q), range(ic.L), range(ic.K), \
                             range(N)), lowBound=0, upBound=1, cat=LpInteger)

# define penalty function for timing targetCluster function
penalties = {}
for q in range(ic.Q):
    for l in range(ic.L):
        for k in range(ic.K):
            penalties[(q, l, k)] = measures.getDzitta_qlk(q, l, k)

# max val of dzitta for normalization
dzittaMax = max(zip(penalties.values(), penalties.keys()))[0]


# define J3 (timing criterion)
problem += lpSum([penalties[(q, l, k)] * v[q][l][k][n] / dzittaMax \
                  for q in range(ic.Q) for l in range(ic.L) for k in range(ic.K) for n in range(N)])

# TODO: here must be determined J1 and J2 criterions


# add constraints
# 0 - only 1 value can be chosen
for q in range(ic.Q):
    for l in range(ic.L):
        for k in range(ic.K):
            problem += lpSum([v[q][l][k] for n in range(N)]) <= 1

# 1 - the sum of UAV is limited on each airport
for q in range(ic.Q):
    for l in range(ic.L):
        problem += lpSum([v[q][l][k][n] * n for k in range(ic.K) for n in range(N)]) <= ic.A_ql[q][l]

# 2 - general sum of UAV is limited
# for q in range(ic.Q):
#     for l in range(ic.L):
#         for k in range(ic.K):




# 3 - non negative is condition is met automatically
# 4 - range condition must be determined as targetCluster function


# save problem
problem.writeLP("UAV scheduling problem.lp")

problem.solve()
print("Status:", LpStatus[problem.status])

# print matrix
for q in range(ic.Q):
    print('Airport {}'.format(q))
    for k in range(ic.K):
        row = ""
        for l in range(ic.L):
            for n in range(N):
                if v[q][l][k][n] == 1:
                    row += str(n)
            row += '\t'
        print(row)

