import logging

# from PySide2 import QtWidgets
from PySide2.QtWidgets import (QGraphicsItem, QGraphicsEllipseItem,
                               QGraphicsSimpleTextItem, QGraphicsLineItem)
from PySide2.QtCore import Qt, QLineF, QPointF, QRectF
from PySide2.QtGui import QPen, QTransform, QBrush, QColor, QFont, qRgb

from dwta import models
from dwta.state import Position2D, Position
from dwta.world import WorldArea


LOG = logging.getLogger(__name__)


class WorldAreaView(QGraphicsItem):

    def __init__(self, world_area, parent=None):
        super().__init__(parent)
        self._world_area = world_area

    def paint(self, painter, style_options, widget=None):
        painter.save()
        painter.setPen(QPen(Qt.black, 3))
        painter.drawRect(self._world_area.area)
        painter.restore()

    def boundingRect(self):
        return self._world_area.area


class VisibilityAreaView(QGraphicsItem):
    def __init__(self, visibility_area, color=None, parent=None):
        super().__init__(parent)

        self.visibility_area = visibility_area
        self.color = QColor(color or self._pick_color())

        self.visibility_area.sigChanged.connect(self.update_area)

    @staticmethod
    def _pick_color():
        return qRgb(0, 0, 0)

    def update_area(self):
        raise NotImplementedError


class CircleAreaView(VisibilityAreaView, QGraphicsEllipseItem):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setPen(QPen(self.color))
        self.update_area()

    def update_area(self):
        x = y = -self.visibility_area.value
        width = height = self.visibility_area.value * 2
        self.setRect(x, y, width, height)


class ActorView(QGraphicsItem):

    MARKER_SIZE = 10
    MARKER_PEN_WIDTH = 1
    FONT_SIZE = 10

    def __init__(self, actor, parent=None, color=None):
        super().__init__(parent)
        self.setFlags(QGraphicsItem.ItemIsSelectable |
                      QGraphicsItem.ItemIsFocusable |
                      QGraphicsItem.ItemIsMovable |
                      QGraphicsItem.ItemSendsGeometryChanges |
                      QGraphicsItem.ItemSendsScenePositionChanges)

        self.actor = actor
        self._visible_scale_factor = 1.0
        self._color = QColor(color or self._pick_color())

        self.actor.sigPositionUpdate.connect(self.update_position)
        self.update_position(actor.position)

        self._marker = QGraphicsEllipseItem(parent=self)
        self._marker.setFlag(QGraphicsItem.ItemIgnoresTransformations)
        marker_pen = QPen(self._color.darker())
        marker_pen.setWidth(self.MARKER_PEN_WIDTH)
        self._marker.setPen(marker_pen)
        self._marker.setRect(self._marker_rect(with_pen=False))
        self._marker.setZValue(0.0)

        self.update_selection()

        self._name_item = QGraphicsSimpleTextItem(parent=self)
        self._name_item.setFlag(QGraphicsItem.ItemIgnoresTransformations)
        self._name_item.setTransform(QTransform().translate(10, 10))
        self._name_item.setFont(QFont('sans-serif', self.FONT_SIZE))
        self._name_item.setText(f'id={self.actor.id}')
        self._name_item.setZValue(0.5)

        self._dragging = False

    @property
    def _name(self):
        return 'actor'

    def _marker_rect(self, with_pen=True):
        size = self.MARKER_SIZE
        if with_pen:
            size += self.MARKER_PEN_WIDTH
        size *= self._visible_scale_factor
        x = y = -size
        width = height = size * 2
        return QRectF(x, y, width, height)

    @staticmethod
    def _pick_color():
        # return np.random.choice(('g', 'c', 'm', 'y', 'k'))
        return qRgb(100, 100, 100)

    def update_position(self, position):
        self.setPos(position.x, position.y)

    def update_actor_position(self, qpoint):
        self.actor.position = Position2D.from_qpoint(qpoint)

    def update_selection(self):
        if self.isSelected():
            self._marker.setBrush(QBrush(Qt.red))
        else:
            self._marker.setBrush(QBrush(self._color))

    def _update_visible_scale_factor(self, transform):
        # FIXME: it's a hack, because we update scale factor based on paint
        #  method calls
        new_scale = self.scale() / transform.m11()
        if new_scale == self._visible_scale_factor:
            return

        self._visible_scale_factor = new_scale

        LOG.debug(f'visible scale factor updated '
                  f'to {self._visible_scale_factor}')

    def paint(self, painter, style_options, widget=None):
        self._update_visible_scale_factor(painter.transform())

    def boundingRect(self):
        return self._marker_rect(with_pen=True)

    def mousePressEvent(self, mouse_event):
        super().mousePressEvent(mouse_event)
        if mouse_event.button() == Qt.MouseButton.LeftButton:
            self._dragging = True

    def mouseMoveEvent(self, mouse_event):
        super().mouseMoveEvent(mouse_event)
        if self._dragging:
            self.update_actor_position(self.pos())

    def mouseDragEvent(self, mouse_event):
        mouse_event.accept()
        if self._dragging:
            self.setPos(self.pos() + mouse_event.pos() - mouse_event.lastPos())

    def mouseReleaseEvent(self, mouse_event):
        super().mouseReleaseEvent(mouse_event)
        if mouse_event.button() == Qt.MouseButton.LeftButton:
            self._dragging = False

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemSceneChange:
            # The item's scene() is the old scene (or 0 if the item has not
            # been added to a scene yet). The value argument is the new scene
            if self.scene():
                self.scene().selectionChanged.disconnect(self.update_selection)

            if value:
                value.selectionChanged.connect(self.update_selection)

        # important: we need to pass any change and value higher. if
        # this wouldn't be done, things can become broken
        return super().itemChange(change, value)


class AgentView(ActorView):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setZValue(10)

        self._visibility_area = create_view(
            self.actor.visibility_area, color=self._color, parent=self)

    @property
    def _name(self):
        return 'agent'


class AutonomousUAVView(AgentView):

    ASSIGNMENT_WIDTH = 2

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._assignment = None
        self.actor.sigNewTargetSelected.connect(self.update_assignement)

    def update_assignement(self):
        if self._assignment:
            self.actor.sigPositionUpdate.disconnect(
                self.update_assignement_position)
            self.scene().removeItem(self._assignment)
            self._assignment = None

        if self.actor.chosen_target and \
                not isinstance(self.actor.chosen_target, models.SearchTarget):
            self._assignment = QGraphicsLineItem(parent=self)
            # self._assignment.setFlag(QGraphicsItem.ItemIgnoresTransformations)
            self._assignment.setPen(QPen(Qt.red, self.ASSIGNMENT_WIDTH))

            self.actor.sigPositionUpdate.connect(
                self.update_assignement_position)
            self.update_assignement_position()

            self.scene().redraw_grid_under_item(self._assignment)

    def update_assignement_position(self):
        target_relative_pos = \
            Position(self.actor.chosen_target.position.coordinates -
                     self.actor.position.coordinates)
        self._assignment.setLine(
            QLineF(QPointF(0, 0), target_relative_pos.as_qpoint()))


class TargetView(ActorView):

    @property
    def _name(self):
        return 'target'

    @staticmethod
    def _pick_color():
        return qRgb(200, 200, 200)


_views = {
    models.AutonomousUAV: AutonomousUAVView,
    models.Target: TargetView,
    models.CircleArea: CircleAreaView,
    WorldArea: WorldAreaView
}


def _get_view_class(obj):
    t = type(obj)
    return _views[t]


def create_view(obj, **kwargs):
    view_class = _get_view_class(obj)
    return view_class(obj, **kwargs)

