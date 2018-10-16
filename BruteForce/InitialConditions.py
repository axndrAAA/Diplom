# в файле содержатся начальные условия, и все необходимые данныне

import numpy as np
import BruteForce.TimeGapClass as tg

L = 3 # - число доступных типов БЛА
K = 4 # - число кластеров целей
Q = 3 # - число аэродромов базирования

#Ценность БЛА типа l
p_l = np.array([0.3, 0.6, 0.8])

#Ценность кластера к как обекта атаки
c_k = np.asarray([0.25, 0.4, 0.9])

# Вероятность уничтожения кластера к(второй индекс) УБЛА типа l(первый индекс)
ro_lk = np.array([[0.78, 0.83, 0.92],[0.95, 0.75, 0.98]]);

# Вероятность потери БЛА типа l при атаке кластера к
r_lk = np.array([[0.4,0.45,0.35],[0.55,0.2,0.49]])

#Координаты аэродромов базирования
X_q = [tg.Point(35.0,5.0),tg.Point(100.0,85.0),tg.Point(5.0,90.0)]

# Доступное для распределения количество БЛА
A_ql = np.array([[2,4,5],[3,2,4],[5,6,8]])

# Координаты Класеров
X_k = [tg.Point(7.0,45.0),tg.Point(40.0,75.0),tg.Point(80.0,42.0),tg.Point(35.0,45.0)]

#временные интервалы нанесения удара по k -му кластеру
T_k = [tg.TimeGap(30,40),tg.TimeGap(48,55),tg.TimeGap(28,35),tg.TimeGap(20,25)]

# Диапозон скоростей БЛА типа l [м/с]
V_l = [tg.VelGap(30.0,45.0),tg.VelGap(50.0,90.0),tg.VelGap(75.0,100.0)]

# Коэффициенты при составляющих критерия
alpha = np.array([0.4,0.6,0.8])

