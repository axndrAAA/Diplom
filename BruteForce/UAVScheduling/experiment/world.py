import logging

from PySide2.QtCore import QObject, Signal, QRectF

from UAVScheduling.models.models import Object


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

    sigObjectAdded = Signal(Object)
    sigObjectRemoved = Signal(Object)

    def __init__(self, objects=None, area=None, parent=None):
        """

        Args:
            objects:
            area (WorldArea):
        """
        super().__init__(parent)

        self._objects = set()
        self._objects_index = 0

        self._objects = area

        self.wait_updates = True

        if objects:
            self.add(objects)

        LOG.info(f'Created World with area {self._area.area} and'
                 f' {len(self._objects)} objects')

    def __repr__(self):
        objects = ', '.join(str(object) for object in self.objects)
        return f'World:\n\tObjects: {objects}'

    def _assign_index(self, object):
        object.in_world_id = self._objects_index
        self._objects_index += 1

    @property
    def objects(self):
        return self._objects

    @property
    def area(self):
        return self._area

    def add(self, objects_array):
        LOG.info(f'Adding {len(objects_array)} objects')
        [self.add_object(object, with_update=False) for object in objects_array]
        self.update()

    def add_object(self, object, with_update=True):
        if not isinstance(object, Object):
            raise WorldError('Only instances of Object can be added '
                             'to the World')
        object.world = self
        self.objects.add(object)
        self._assign_index(object)

        LOG.debug(f'Added new object: {object}')

        # for consistency, we update states of all objects in World on changes
        #  in Object's state (position)
        object.sigPositionUpdate.connect(self.update)

        if with_update:
            self.update()

        self.sigObjectAdded.emit(object)

    def remove(self, objects_array):
        LOG.info(f'Removing {len(objects_array)} objects')
        [self.remove_object(object, with_update=False) for object in objects_array]
        self.update()

    def remove_object(self, object, with_update=True):
        try:
            LOG.debug(f'Removing {objects}')

            self._objects.remove(object)
            object.world = None

            if with_update:
                self.update()

            self.sigObjectRemoved.emit(object)
        except ValueError:
            raise WorldError('Object not found in this World')

    def clear(self):
        for object in self._objects:
            self.remove_object(object, with_update=False)

    def get_objects(self, object_type):
        """Returns all objects of concrete type"""
        # TODO: can add str argument support
        return [object for object in self._objects
                if isinstance(object, object_type)]

    def update(self):
        LOG.debug('World update started')
        for object in self.objects:
            object.update_state()
        LOG.debug('World update finished')
