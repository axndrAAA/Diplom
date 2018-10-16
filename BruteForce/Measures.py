import BruteForce.InitialConditions as ic


def J1(x_lkq):
    m = 1
    sum = 0
    for k in range(ic.K):
        for l in range(ic.L):
            for q in range(ic.Q):
                m *= ((1 - ic.ro_lk[l,k])**x_lkq[l,k,q])

        sum += ic.c_k[k]*(1 - m)/ic.c_k.max()
    return sum/ic.K


def J2(x_lkq):
    d_sum = 0.0
    for k in range(ic.K):
        for l in range(ic.L):
            for q in range(ic.Q):
                d_sum += ic.p_l[l] * ic.r_lk[l,k]*x_lkq[l,k,q]/ic.p_l.max()
    return d_sum/x_lkq.sum()


def J3(x_lkq):
    return 1

def J(x_lkq):
    return ic.alpha[0]*J1(x_lkq) - ic.alpha[1]*J2(x_lkq) + ic.alpha[2]*J3(x_lkq)
