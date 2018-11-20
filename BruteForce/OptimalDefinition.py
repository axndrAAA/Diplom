import  numpy as np
import Measures as criteria
import SimpleInitialConditions as ic

class OptimalDefinition:
    J_max = -1000
    X_lkq_optimal = 0
    counter = 0

    def __init__(self):
        self.X_lkq_optimal = np.zeros((ic.L, ic.K, ic.Q))

    def checkMatrix(self, X_lkq):
        # счетчик вызова функции
        self.counter += 1

        # проверка выполнения ограничения по дальности
        # if not criteria.checkDistances(X_lkq):
        #     return
        # вычисление значения критерия
        J = criteria.J(X_lkq)
        if J > self.J_max:
            self.J_max = J
            self.X_lkq_optimal = X_lkq.copy()
        else:
            return
