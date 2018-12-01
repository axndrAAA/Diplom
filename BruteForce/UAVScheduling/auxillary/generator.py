import numpy as np

from UAVScheduling.models import models
from UAVScheduling.auxillary.state import Position2D


class Generator(object):

    def __init__(self, positions_area, seed=None):
        self._random = np.random.RandomState(seed or 27644437)

        self._positions_area = positions_area

    def position(self):
        min_x = self._positions_area.area.left()
        max_x = self._positions_area.area.right()

        min_y = self._positions_area.area.bottom()
        max_y = self._positions_area.area.top()

        x = self._random.uniform(min_x, max_x)
        y = self._random.uniform(min_y, max_y)
        return Position2D(x, y)

    def airport(self, **params):
        position = self.position()
        return models.Airport(position, **params)

    def target_value(self, min, max):
        if min < 0:
            min = 0
        return self._random.uniform(min, max)

    def targetCluster(self, value, random=False, **kwargs):
        if random:
            value = self.target_value(0, value)
        position = self.position()
        return models.TargetCluster(position, value=value)

    def many(self, _type, num, *args, **kwargs):
        if _type == 'airport':
            method = self.airport
        elif _type == 'targetCluster':
            method = self.targetCluster
        elif _type in ['pos', 'position']:
            method = self.position
        else:
            raise ValueError(f'{_type} is unknown')
        return {method(*args, **kwargs) for _ in range(num)}
