import numpy as np
from numpy import linalg

from PySide2.QtCore import QPointF


class Position(object):
    """Represents position in `World`"""

    def __init__(self, coordinates):
        self.coordinates = np.asarray(coordinates)

    def __repr__(self):
        coordinates = ','.join(f'{coord:.2f}' for coord in self.coordinates)
        return f'({coordinates})'

    @property
    def x(self):
        return self.coordinates[0]

    @property
    def y(self):
        return self.coordinates[1]

    def as_qpoint(self):
        return QPointF(self.x, self.y)

    @staticmethod
    def from_qpoint(qpoint):
        return Position2D(qpoint.x(), qpoint.y())


def get_distance(pos1, pos2):
    """

    Args:
        pos1 (Position):
        pos2 (Position):
    """
    vec = pos1.coordinates - pos2.coordinates
    return linalg.norm(vec)


class Position2D(Position):

    # TODO: maybe add more efficient norm for 2D vector

    def __init__(self, x, y):
        super().__init__((x, y))


class VelosityRange:
    def __init__(self, _v_min,_v_max):
        self.v_min = _v_min
        self.v_max = _v_max
