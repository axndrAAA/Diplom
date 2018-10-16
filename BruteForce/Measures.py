import BruteForce.InitialConditions as ic
import math as m


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
    sum = 0
    for k in range(ic.K):
        for l in range(ic.L):
            for q in range(ic.Q):
                sum += x_lkq[l,k,q]*getDzitta_qkl(q,k,l)/(ic.T_k[k].t_max - ic.T_k[k].t_min)

    sum /= x_lkq.sum()
    return sum

def J(x_lkq):
    return ic.alpha[0]*J1(x_lkq) - ic.alpha[1]*J2(x_lkq) + ic.alpha[2]*J3(x_lkq)

def getDzitta_qkl(q,k,l):
    d_qk = getD_qk(q,k)
    ret =  0.5*((d_qk/ic.V_l[l].v_min - d_qk/ic.V_l[l].v_max) + (ic.T_k[k].t_max - ic.T_k[k].t_min)
                - m.fabs(ic.T_k[k].t_min -  d_qk/ic.V_l[l].v_max)-m.fabs(ic.T_k[k].t_max -  d_qk/ic.V_l[l].v_min))
    return ret

def getD_qk(q,k):
    return m.sqrt(m.pow((ic.X_q[q].x - ic.X_k[k].x),2) + m.pow((ic.X_q[q].y - ic.X_k[k].y),2))