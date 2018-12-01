import abc
import logging


import numpy as np
from PySide2.QtCore import QObject, Signal

from UAVScheduling.auxillary.state import get_distance, Position, Position2D, VelosityRange


LOG = logging.getLogger(__name__)

def with_probability(prob):
    """Returns True with probability ``prob``."""
    return np.random.uniform() <= prob

class VisibilityArea(QObject):

    sigChanged = Signal()

    def __init__(self, center=None, parent=None):
        super().__init__(parent)
        self.center = center or Position2D(0, 0)

        self._attrib = {'center': 'center'}

    def set_center(self, value):
        self.center = value

    @property
    def value(self):
        raise NotImplementedError

    def _get_fields(self):
        fields = self.__dict__
        return {name: fields[field] for field, name in self._attrib.items()}

    def copy(self):
        T = type(self)
        return T(**self._get_fields(), parent=self.parent())

    def covers(self, position):
        raise NotImplementedError

class CircleArea(VisibilityArea):
    def __init__(self, radius=10, **kwargs):
        super().__init__(**kwargs)
        self._radius = radius

        self._attrib['_radius'] = 'radius'

    @property
    def value(self):
        return self._radius

    @property
    def radius(self):
        return self._radius

    def set_radius(self, value):
        if self._radius == value:
            return

        self._radius = value
        self.sigChanged.emit()

    def covers(self, position):
        return get_distance(self.center, position) < self._radius

class Object(QObject):
    """Entity that interacts with the ``World`` and other ``Objects``.

    Attributes:
        in_world_id: id number in the ``World`` where this ``Object`` were
            assigned.
    """

    sigPositionUpdate = Signal(Position)

    def __init__(self, position=None, parent=None):
        """

        Args:
            position (Position): Initial position of ``Object``.
        """
        super().__init__(parent)
        self._position = position or Position2D(0, 0)
        self._world = None
        self.in_world_id = -1  # TODO: who need to set this?

    def __repr__(self):
        main_part = f'{self.full_name} {str(self.position)}'
        if self.details:
            main_part += ' ' + self.details
        return f'<{main_part}>'

    @property
    def full_name(self):
        return f'{self.name} #{self.id:02}'

    @property
    def name(self):
        return type(self).__name__

    @property
    def details(self):
        return ''

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        if self._position == value:
            return

        self._position = value
        LOG.debug(f'Position updated to {value}')
        if self._world.wait_updates:
            self.sigPositionUpdate.emit(self._position)

    @property
    def world(self):
        return self._world

    @world.setter
    def world(self, value):
        self._world = value
        if not self.world:
            self.in_world_id = -1

    @property
    def id(self):
        """Alias for ``in_world_id``."""
        return self.in_world_id

    def get_distance_to(self, object):
        return get_distance(self.position, object.position)

    @abc.abstractmethod
    def update_state(self):
        """Updates state of ``Object`` according to changes in ``World``."""
        LOG.debug(f'Updating state for {self.full_name}')

class Airport(Object):

    sigValueChanged = Signal(float)

    def __init__(self, *args, value=1.0, **kwargs):
        super().__init__(*args, **kwargs)

        self._value = value
        self.state = None

    @property
    def details(self):
        return f'value = {self.value}'

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if value == self._value:
            return

        self._value = value
        LOG.info(f'Value for {self.full_name} is set to {value}')
        self.sigValueChanged.emit(value)

class TargetCluster(Object):

    sigValueChanged = Signal(float)

    def __init__(self, *args, value=1.0, **kwargs):
        super().__init__(*args, **kwargs)

        self._value = value
        self.state = None

    @property
    def details(self):
        return f'value = {self.value}'

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if value == self._value:
            return

        self._value = value
        LOG.info(f'Value for {self.full_name} is set to {value}')
        self.sigValueChanged.emit(value)

class UAVType(Object):

    sigCostChanged = Signal(float)
    sigCVelRangeChanged = Signal(VelosityRange)
    sigRadiusChanged = Signal(float)

    def __init__(self, cost=0.5, vel_range=None, radius=0):

        self._cost = cost
        self._radius = radius
        self._vel_range = vel_range

    @property
    def cost(self):
        return self._cost

    @cost.setter
    def cost(self, cost):
        if cost == self._cost:
            return

        self._cost = cost
        self.sigCostChanged.emit(cost)

    @property
    def velRange(self):
        return self._vel_range

    @velRange.setter
    def velRange(self, vel_range):
        if vel_range == self._vel_range:
            return
        self._vel_range = vel_range
        self.sigCVelRangeChanged.emit(vel_range)

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, radius):
        if radius == self._radius:
            return

        self._radius = radius
        self.sigRadiusChanged.emit(radius)
