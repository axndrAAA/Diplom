import logging

import numpy as np

from PySide2.QtGui import QColor, QPen, QPicture, QPainter
from PySide2.QtCore import QPointF, qInstallMessageHandler

from dwta.interface.ui_graphics_item import UIGraphicsItem


# to suppress `QPicture: invalid format version 0` warning, caused by PySide
# see: https://groups.google.com/forum/#!msg/pyqtgraph/dYDRWVORxWg/NVV84upli1IJ
qInstallMessageHandler(lambda *args: None)


LOG = logging.getLogger(__name__)


class GridItem(UIGraphicsItem):
    """Displays a rectangular grid of lines indicating major divisions within
    a coordinate system.

    Automatically determines what divisions to use.
    """

    TEXT_DISPLACEMENT = QPointF(0.5, 0.5)
    GRID_SCALES = [2, 1, 0]  # from smaller to bigger cells

    def __init__(self, view_widget, parent=None):
        super().__init__(view_widget, parent)
        self.picture = None
        self._painter = None
        self._texts = []

        self.p1 = np.array([0., 0.])
        self.p2 = np.array([0., 0.])

    def paint(self, painter, style_options, widget=None):
        if self.picture is None:
            self.generatePicture()

        LOG.debug('Drawing grid...')
        painter.drawPicture(QPointF(0, 0), self.picture)

    def viewRangeChanged(self):
        super().viewRangeChanged()
        self.picture = None

    def generatePicture(self):
        self.picture = QPicture()
        self._painter = QPainter()
        self._painter.begin(self.picture)

        self._read_dimensions()
        distances = self._br - self._ul

        self._texts = []
        for scale in self.GRID_SCALES:
            self._draw_grid_scale(scale, distances)

        self._draw_texts()
        self._painter.end()

        LOG.debug('Generated new grid')

    def _draw_grid_scale(self, scale, distances):
        self._current_scale = scale

        nlTarget = 10. ** self._current_scale
        self._delta = 10. ** np.floor(np.log10(abs(distances / nlTarget)) + 0.5)

        self._ul1 = np.floor(self._ul / self._delta) * self._delta
        br1 = np.ceil(self._br / self._delta) * self._delta
        distances = br1 - self._ul1
        self._lines_number_per_axis = (distances / self._delta) + 0.5

        for ax in range(0, 2):  # Draw grid for both axes
            self._draw_axes(ax)

    def _draw_axes(self, ax):
        self._current_ax = ax
        self._current_bx = (self._current_ax + 1) % 2

        self._compute_alpha()
        self._set_line_pen()

        lines_number = int(self._lines_number_per_axis[self._current_ax])
        for line_num in range(0, lines_number):
            self._eval_points(line_num)
            if self._draw_lines():
                self._create_text()

    def _eval_points(self, line_num):
        ax = self._current_ax
        bx = self._current_bx

        self.p1[ax] = self._ul1[ax] + line_num * self._delta[ax]
        self.p1[bx] = self._ul[bx]

        self.p2[ax] = self.p1[ax]
        self.p2[bx] = self._br[bx]

    def _draw_lines(self):
        # don't draw lines that are out of bounds.
        # if self._check_out_of_bounds(self.p1):
        #     return False

        # NOTE: it is important that line points are defined with QPointF.
        #  if we use drawLine(int x1, int y1, int x2, int y2) instead, then
        #  we couldn't see grid with step less than 1!
        self._painter.drawLine(QPointF(self.p1[0], self.p1[1]),
                               QPointF(self.p2[0], self.p2[1]))
        return True

    def _create_text(self):
        if 2 <= self._current_scale:
            return

        if self._current_ax == 0:
            x = self.p1[0] + self.pixel_width
            y = self._ul[1] + self.pixel_height * 8.
        else:
            x = self._ul[0] + self.pixel_width * 3.
            y = self.p1[1] + self.pixel_height

        self._texts.append((QPointF(x, y), "%g" % self.p1[self._current_ax]))

    def _draw_texts(self):
        self._set_text_pen()
        self._painter.setWorldTransform(self.invertedDeviceTransform)
        for t in self._texts:
            x = self.deviceTransform.map(t[0]) + self.TEXT_DISPLACEMENT
            self._painter.drawText(x, t[1])

    # NOTE: this check is not so necessary, since most of the time we have,
    #  lines that are visible
    # def _check_out_of_bounds(self, point):
    #     ax = self._current_ax
    #     return not (min(self._ul[ax], self._br[ax])
    #                 <= point[ax]
    #                 <= max(self._ul[ax], self._br[ax]))

    def _read_dimensions(self):
        visible_rect = self._view_widget.rect()
        self._visible_dimensions = [visible_rect.width(), visible_rect.height()]

        rect_in_scene = self._view_widget.getVisibleRect()
        self._ul = np.array([rect_in_scene.left(), rect_in_scene.top()])
        self._br = np.array([rect_in_scene.right(), rect_in_scene.bottom()])

        self._check_y_axis_orientation()

    def _check_y_axis_orientation(self):
        if self._br[1] < self._ul[1]:
            # swap values
            temp = self._ul[1]
            self._ul[1] = self._br[1]
            self._br[1] = temp

    def _set_line_pen(self):
        linePen = QPen(QColor(0, 0, 0, self._alpha))
        linePen.setCosmetic(False)
        if self._current_ax == 0:
            linePen.setWidthF(self.pixel_width)
        else:
            linePen.setWidthF(self.pixel_height)
        self._painter.setPen(linePen)

    def _set_text_pen(self):
        textPen = QPen(QColor(0, 0, 0, self._alpha * 2))
        self._painter.setPen(textPen)

    def _compute_alpha(self):
        ax = self._current_ax
        ppl = self._visible_dimensions[ax] / self._lines_number_per_axis[ax]
        self._alpha = np.clip(3. * (ppl - 3), 0., 30.)
