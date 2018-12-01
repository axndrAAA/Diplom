from PySide2.QtCore import Qt, QPoint, QRectF, Signal
from PySide2.QtGui import QMatrix, QPainter
from PySide2.QtWidgets import QGraphicsView


class MyView(QGraphicsView):

    INIT_ZOOM = 250
    ZOOM_DELTA = 6

    sigRangeChanged = Signal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setRenderHint(QPainter.Antialiasing)
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.setViewportUpdateMode(QGraphicsView.SmartViewportUpdate)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)

        self._zoom_value = self.INIT_ZOOM

        self._dragging = False

        self._setup_matrix()

    def _setup_matrix(self):
        scale = pow(2.0, (self._zoom_value - self.INIT_ZOOM) / 50.0)
        matrix = QMatrix()
        matrix.scale(scale, -scale)  # NOTE: y axis is flipped
        self.setMatrix(matrix)
        self.sigRangeChanged.emit()

    def setScene(self, scene):
        self.fitInView(scene.itemsBoundingRect(), Qt.KeepAspectRatio)
        super().setScene(scene)

    def getVisibleRect(self):
        # see: https://stackoverflow.com/a/10849582/10380652
        a = self.mapToScene(QPoint(0, 0))
        b = self.mapToScene(QPoint(self.viewport().width(),
                                   self.viewport().height()))
        return QRectF(a, b)

    def wheelEvent(self, event):
        event.accept()
        if event.delta() > 0:
            if 3 * self.INIT_ZOOM < self._zoom_value:
                return
            self._zoom_value += self.ZOOM_DELTA
        else:
            if self._zoom_value < -self.INIT_ZOOM:
                return
            self._zoom_value -= self.ZOOM_DELTA
        self._setup_matrix()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.sigRangeChanged.emit()

    def mousePressEvent(self, mouse_event):
        super().mousePressEvent(mouse_event)
        if mouse_event.button() == Qt.MouseButton.LeftButton:
            self._dragging = True

    def mouseMoveEvent(self, mouse_event):
        super().mouseMoveEvent(mouse_event)
        if self._dragging:
            self.sigRangeChanged.emit()

    def mouseReleaseEvent(self, mouse_event):
        super().mouseReleaseEvent(mouse_event)
        if mouse_event.button() == Qt.MouseButton.LeftButton:
            self._dragging = False

    def scrollContentsBy(self, dx, dy):
        # NOTE: we need separate handler for scroll bars
        super().scrollContentsBy(dx, dy)
        self.sigRangeChanged.emit()
