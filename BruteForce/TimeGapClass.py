class TimeGap:
    t_min = 0
    t_max = 0

    def __init__(self, _timn, _tmax):
        self.t_min = _timn * 60
        self.t_max = _tmax * 60

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
        self.x = _x
        self.y = _y

