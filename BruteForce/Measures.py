import InitialConditions.InitialConditions2 as ic
import math as m

def J1(x_qlk):
    sum = 0
    c_k_max = ic.c_k.max()
    for k in range(ic.K):
        m = 1
        for l in range(ic.L):
            for q in range(ic.Q):
                m *= ((1 - ic.ro_lk[l, k]) ** x_qlk[q, l, k])
        sum += ic.c_k[k]*(1 - m)/c_k_max
    return sum/ic.K

def J2(x_qlk):
    d_sum = 0.0
    p_l_max = ic.p_l.max()
    for k in range(ic.K):
        for l in range(ic.L):
            for q in range(ic.Q):
                d_sum += ic.p_l[l] * ic.r_lk[l, k] * x_qlk[q, l, k] / p_l_max
    sm = x_qlk.sum()
    if sm > 0:
        return d_sum / sm
    else:
        return d_sum

def J3(x_qlk):
    sum = 0
    for k in range(ic.K):
        for l in range(ic.L):
            for q in range(ic.Q):
                sum += x_qlk[q, l, k] * getDzitta_qlk(q, l, k) / (ic.T_k[k].t_max - ic.T_k[k].t_min)
    sm = x_qlk.sum()
    if (sm > 0):
        return sum / sm
    else:
        return sum

def J(x_qlk):
    return ic.alpha[0] * J1(x_qlk) - ic.alpha[1] * J2(x_qlk) + ic.alpha[2] * J3(x_qlk)

def getDzitta_qlk(q, l, k):
    d_qk = getD_qk(q, k)
    ret = 0.5*((d_qk/ic.V_l[l].v_min - d_qk/ic.V_l[l].v_max) + (ic.T_k[k].t_max - ic.T_k[k].t_min)
                - m.fabs(ic.T_k[k].t_min - d_qk/ic.V_l[l].v_max) - m.fabs(ic.T_k[k].t_max - d_qk/ic.V_l[l].v_min))
    return ret

def getD_qk(q, k):
    return m.sqrt(m.pow((ic.X_q[q].x - ic.X_k[k].x),2) + m.pow((ic.X_q[q].y - ic.X_k[k].y),2))


def checkDistance(l, q, k):
    d_kq = m.sqrt(m.pow(ic.X_k[k].x - ic.X_q[q].x, 2)+m.pow(ic.X_k[k].y - ic.X_q[q].y, 2))
    if(d_kq > ic.R_l[l]):
        return False
    else:
        return True

def checkDistances(x_lkq):
    for q in range(ic.Q):
        for l in range(ic.L):
            for k in range(ic.K):
                if x_lkq[q, l, k] > 0:
                    d_kq = m.sqrt(m.pow(ic.X_k[k].x - ic.X_q[q].x, 2) + m.pow(ic.X_k[k].y - ic.X_q[q].y, 2))
                    if d_kq > ic.R_l[l]:
                        return False
    return True

def checkDistanceConstraint(q, l, m):
    ret = []
    for n in range(len(m)):
        flag = True
        for k in range(len(m[n])):
            if m[n][k] > 0:
                if not checkDistance(l, q, k):
                    flag = False
                    break
        if flag:
            ret.append(m[n])
    return ret
