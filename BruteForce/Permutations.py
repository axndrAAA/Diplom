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
            # last = self.lst.pop()
            # arr = np.zeros(len(last))
            # for i in range(arr.size):
            #     arr[i] = int(last[i])
            # if(arr.sum() <= self.sum_condition):
            #     ret.append(arr)
        return ret


