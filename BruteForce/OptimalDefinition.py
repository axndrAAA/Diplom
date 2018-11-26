import  numpy as np
import Measures as measures
from Measures import *

class OptimalDefinition:
    J_max = -1000
    X_qlk_optimal = 0
    counter = 0

    def __init__(self):
        self.X_qlk_optimal = np.zeros((ic.L, ic.K, ic.Q))

    def checkMatrix(self, X_qlk):
        # счетчик вызова функции
        self.counter += 1

        # проверка выполнения ограничения по дальности
        # if not criteria.checkDistances(X_lkq):
        #     return
        # вычисление значения критерия
        J = measures.J(X_qlk)
        if J > self.J_max:
            self.J_max = J
            self.X_qlk_optimal = X_qlk.copy()
        else:
            return
