class TimeGap:
    t_min = 0
    t_max = 0

    def __init__(self, _timn, _tmax):
        #хранится в секундах
        self.t_min = _timn
        self.t_max = _tmax

class VelGap:
    v_min = 0
    v_max = 0
    def __init__(self, _v_min,_v_max):
        self.v_min = _v_min
        self.v_max = _v_max

class Point:
    x = 0
    y = 0
    def __init__(self, _x, _y):
        # передается в километрах, хранится и используется в метрах
        self.x = _x * 1000.0
        self.y = _y * 1000.0

