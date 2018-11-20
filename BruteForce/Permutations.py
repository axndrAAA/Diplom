#класс будет выдавать все возможные комбинации последовательностей чисел, для которых сумма не будет превышать заданного числа
import  numpy as np
import itertools as it
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
        nl_indexes = np.ones(len(prmts_ln), dtype=np.int)*-1
        groups_cnt = len(prmts_ln)
        while True:
            if l == groups_cnt - 1:
                for nl_indexes[l] in range(len(prmts_ln[l])):
                    x[l] = prmts_ln[l][nl_indexes[l]]
                    ret.append(np.array(x))
                    if nl_indexes[0] == 70:
                        l=l
                l -= 1
            else:
                if nl_indexes[l] < len(prmts_ln[l])-1:
                    nl_indexes[l] += 1
                    x[l] = prmts_ln[l][nl_indexes[l]]
                    l += 1
                else:
                    nl_indexes[l] = -1
                    l -= 1

            # условие выхода
            if nl_indexes[0] == -1:  # nl_indexes[0] == len(prmts_ln[0]):
                break

        return ret
