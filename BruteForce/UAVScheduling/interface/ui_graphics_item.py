from PySide2.QtCore import QRectF, QLineF
# from PySide2.QtGui import QPainterPathStroker
from PySide2.QtWidgets import QGraphicsObject


class UIGraphicsItem(QGraphicsObject):
    """
    Base class for graphics items with boundaries relative to a GraphicsView or ViewBox.
    The purpose of this class is to allow the creation of GraphicsItems which live inside
    a scalable view, but whose boundaries will always stay fixed relative to the view's boundaries.
    For example: GridItem, InfiniteLine

    The view can be specified on initialization or it can be automatically detected when the item is painted.

    NOTE: Only the item's boundingRect is affected; the item is not transformed
     in any way. Use viewRangeChanged to respond to changes in the view.
    """

    def __init__(self, view_widget, parent=None):
        super().__init__(parent)
        self.setFlag(self.ItemSendsScenePositionChanges)

        self._view_widget = view_widget
        self._view_widget.sigRangeChanged.connect(self.viewRangeChanged)

        self._boundingRect = None

        self._viewport_transform = None
        self._dt = None

    def itemChange(self, change, value):
        ret = super().itemChange(change, value)

        if change == self.ItemScenePositionHasChanged:
            self.setNewBounds()
        return ret

    def setPos(self, *args):
        super().setPos(*args)
        self.setNewBounds()

    def boundingRect(self):
        if not self._boundingRect:
            self._boundingRect = self._view_widget.getVisibleRect()
        return self._boundingRect

    def viewRangeChanged(self):
        """Called when the view widget/viewbox is resized/rescaled"""
        self.setNewBounds()
        self.update()

    def setNewBounds(self):
        """Update the item's bounding rect to match the viewport"""
        # invalidate bounding rect, regenerate later if needed.
        self._boundingRect = None
        self.prepareGeometryChange()

    @property
    def deviceTransform(self):
        _viewport_transform = self._view_widget.viewportTransform()
        if self._viewport_transform != _viewport_transform:
            self._viewport_transform = _viewport_transform
            self._dt = super().deviceTransform(_viewport_transform)
        return self._dt

    @property
    def invertedDeviceTransform(self):
        return self.deviceTransform.inverted()[0]

    @property
    def pixel_width(self):
        return self.invertedDeviceTransform.map(QLineF(0, 0, 1, 0)).length()

    @property
    def pixel_height(self):
        return self.invertedDeviceTransform.map(QLineF(0, 0, 0, 1)).length()
