import logging

from PySide2.QtCore import QObject, Signal, QRectF

from dwta.models import Actor


LOG = logging.getLogger(__name__)


class WorldError(Exception):
    pass


class WorldArea(QObject):

    sigChanged = Signal(QRectF)
    sigXChanged = Signal(int)
    sigYChanged = Signal(int)
    sigWidthChanged = Signal(int)
    sigHeightChanged = Signal(int)

    def __init__(self, *args, parent=None):
        """

        Args:
            *args: Could be any args acceptable by QRectF
            parent:
        """
        super().__init__(parent)

        self._rect = QRectF(*args)

    def _setter(self, set_method, new_value, current_value, signal):
        if current_value == new_value:
            return

        set_method(new_value)
        signal.emit(new_value)
        self.sigChanged.emit(self._rect)

    @property
    def area(self):
        return self._rect

    def set_area(self, value):
        self._rect = value
        self.sigChanged.emit(value)

    @property
    def x(self):
        return self._rect.x()

    def set_x(self, value):
        self._setter(self._rect.setX, value,
                     self.x, self.sigXChanged)

    @property
    def y(self):
        return self._rect.y()

    def set_y(self, value):
        self._setter(self._rect.setY, value,
                     self.y, self.sigYChanged)

    @property
    def width(self):
        return self._rect.width()

    def set_width(self, value):
        self._setter(self._rect.setWidth, value,
                     self.width, self.sigWidthChanged)

    @property
    def height(self):
        return self._rect.height()

    def set_height(self, value):
        self._setter(self._rect.setHeight, value,
                     self.height, self.sigHeightChanged)


class World(QObject):
    """Represents a place where all interactions occurs"""

    # TODO: add parameter to temporally disable call to update

    sigActorAdded = Signal(Actor)
    sigActorRemoved = Signal(Actor)

    def __init__(self, actors=None, area=None, parent=None):
        """

        Args:
            actors:
            area (WorldArea):
        """
        super().__init__(parent)

        self._actors = set()
        self._actors_index = 0

        self._area = area

        self.wait_updates = True

        if actors:
            self.add(actors)

        LOG.info(f'Created World with area {self._area.area} and'
                 f' {len(self._actors)} actors')

    def __repr__(self):
        actors = ', '.join(str(actor) for actor in self.actors)
        return f'World:\n\tActors: {actors}'

    def _assign_index(self, actor):
        actor.in_world_id = self._actors_index
        self._actors_index += 1

    @property
    def actors(self):
        return self._actors

    @property
    def area(self):
        return self._area

    def add(self, actors_array):
        LOG.info(f'Adding {len(actors_array)} actors')
        [self.add_actor(actor, with_update=False) for actor in actors_array]
        self.update()

    def add_actor(self, actor, with_update=True):
        if not isinstance(actor, Actor):
            raise WorldError('Only instances of Actor can be added '
                             'to the World')
        actor.world = self
        self.actors.add(actor)
        self._assign_index(actor)

        LOG.debug(f'Added new actor: {actor}')

        # for consistency, we update states of all actors in World on changes
        #  in Actor's state (position)
        actor.sigPositionUpdate.connect(self.update)

        if with_update:
            self.update()

        self.sigActorAdded.emit(actor)

    def remove(self, actors_array):
        LOG.info(f'Removing {len(actors_array)} actors')
        [self.remove_actor(actor, with_update=False) for actor in actors_array]
        self.update()

    def remove_actor(self, actor, with_update=True):
        try:
            LOG.debug(f'Removing {actor}')

            self._actors.remove(actor)
            actor.world = None

            if with_update:
                self.update()

            self.sigActorRemoved.emit(actor)
        except ValueError:
            raise WorldError('Actor not found in this World')

    def clear(self):
        for actor in self._actors:
            self.remove_actor(actor, with_update=False)

    def get_actors(self, actor_type):
        """Returns all actors of concrete type"""
        # TODO: can add str argument support
        return [actor for actor in self._actors
                if isinstance(actor, actor_type)]

    def update(self):
        LOG.debug('World update started')
        for actor in self.actors:
            actor.update_state()
        LOG.debug('World update finished')
