#класс будет выдавать все возможные комбинации последовательностей чисел, для которых сумма не будет превышать заданного числа
import  numpy as np
import itertools as it
class Permutation:
    sum_condition = 0
    lst = 0
    def __init__(self,size, Sum):
        self.sum_condition = Sum
        parameter =''
        for i in range(Sum):
            parameter += str(i)
        self.lst = list(it.combinations_with_replacement(parameter, size))

    def getNext(self):

        while len(self.lst) > 0:
            last = self.lst.pop()
            arr = np.zeros(len(last))
            for i in range(arr.size):
                arr[i] = int(last[i])
            if(arr.sum() <= self.sum_condition):
                return arr
        return None
    def getAll(self):
        ret = []
        while len(self.lst) > 0:
            last = self.lst.pop()
            arr = np.zeros(len(last))
            for i in range(arr.size):
                arr[i] = int(last[i])
            if(arr.sum() <= self.sum_condition):
                ret.append(arr)
        return ret
