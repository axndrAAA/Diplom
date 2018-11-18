#класс будет выдавать все возможные комбинации последовательностей чисел, для которых сумма не будет превышать заданного числа
import  numpy as np
import itertools as it
import InitialConditions as ic
class Permutation:
    sum_condition = 0
    lst = 0
    def __init__(self,size, Sum):
        self.sum_condition = Sum
        parameter = list(range(Sum+1));
        # self.lst = list(it.combinations_with_replacement(parameter, size))
        self.lst = list(it.product(parameter, repeat=size))
    def getNext(self):

        while len(self.lst) > 0:
            last = np.array(self.lst.pop())
            if(last.sum() <= self.sum_condition):
                return last
        return None

    def getAll(self):
        ret = []
        while True:
            arr = self.getNext()
            if(not arr.any()):
               break
            ret.append(arr);
        return ret

    @staticmethod
    def permute(prmts_ln):
        """
            permute возвращает все возможные комбинации каждого элемента c каждым эелементом из всех групп L
            prmts_ln - содержит массивы возможных распределений для каждого типа l

        """

        ret = []
        x = [0] * len(prmts_ln)

        l = 0
        nl_indexes = np.zeros(len(prmts_ln), dtype=np.int)

        while True:
            if l == ic.L - 1:
                for nl_indexes[l] in range(len(prmts_ln[l])):
                    x[l] = prmts_ln[l][nl_indexes[l]]
                    ret.append(np.array(x))
                l -= 1
            else:
                if nl_indexes[l] < len(prmts_ln[l]):
                    x[l] = prmts_ln[l][nl_indexes[l]]
                    nl_indexes[l] += 1
                    l += 1

                else:
                    nl_indexes[l] = 0
                    l -= 1

            # условие выхода
            if nl_indexes[0] == len(prmts_ln[0]):
                break

        return ret
