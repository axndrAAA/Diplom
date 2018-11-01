# в файле содержатся начальные условия, и все необходимые данныне

import numpy as np
import TimeGapClass as tg

L = 3 # - число доступных типов БЛА
K = 4 # - число кластеров целей
Q = 3 # - число аэродромов базирования

#Ценность БЛА типа l
p_l = np.array([0.7, 0.8, 0.9])

#Ценность кластера к как обекта атаки
c_k = np.array([0.95, 0.75, 0.9, 0.93])

# Вероятность уничтожения кластера к(второй индекс) УБЛА типа l(первый индекс)
ro_lk = np.array([[0.78, 0.83, 0.92, 0.92], [0.95, 0.75, 0.98, 0.89], [0.79, 0.83, 0.95, 0.94]])

# Вероятность потери БЛА типа l при атаке кластера к
r_lk = np.array([[0.72, 0.86, 0.90, 0.74], [0.75, 0.65, 0.79, 0.69], [0.75, 0.68, 0.89, 0.71]])

# Доступное для распределения количество БЛА
A_ql = np.array([[2,4,5],[3,2,4],[5,6,8]])

# Коэффициенты при составляющих критерия
alpha = np.array([0.4,0.6,0.8])

#Координаты аэродромов базирования[км]
X_q = [tg.Point(5.0,35.0),tg.Point(100.0,85.0),tg.Point(5.0,90.0)]

# Координаты Класеров[км]
X_k = [tg.Point(7.0,45.0),tg.Point(40.0,75.0),tg.Point(80.0,42.0),tg.Point(35.0,45.0)]

#временные интервалы нанесения удара по k -му кластеру [c] - с момента вылета первого БЛА
T_k = [tg.TimeGap(700,1000),tg.TimeGap(600,900),tg.TimeGap(500,800),tg.TimeGap(650,950)]

# Диапозон скоростей БЛА типа l [м/с]
V_l = [tg.VelGap(30.0,45.0),tg.VelGap(50.0,90.0),tg.VelGap(75.0,100.0)]

#Радиусы боевого Действия БЛА типа l[м]
R_l = np.array([45000, 75000, 100000])

