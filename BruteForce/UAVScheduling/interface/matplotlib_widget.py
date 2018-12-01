from PySide2.QtWidgets import QWidget, QSizePolicy, QVBoxLayout

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)


class PlotCanvas(FigureCanvas):
    """Matplotlib integration in Qt.

    Use `PlotCanvas.axes` in the same way as `matplotlib.axes.Axes`. After any
    plotting call `PlotCanvas.draw()` method.

    Note: this class is subclassed from QWidget, so it could be used as regular
     widget.

    To integrate this widget in GUI with Qt Designer, add empty Widget and
    call "Promote to..." where select this class.

    Attributes:
        ax (matplotlib.axes.Axes):
        figure (matplotlib.figure.Figure):
    """

    def __init__(self, parent=None):
        # a figure instance to plot on
        self.fig = Figure()

        # create an axis
        self.ax = self.fig.add_subplot(111)

        super().__init__(self.fig)
        self.setParent(parent)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.updateGeometry()


class CanvasWithNavigation(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.canvas = PlotCanvas(self)

        # takes the Canvas widget and a parent
        self.toolbar = NavigationToolbar(self.canvas, self)

        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        layout.addWidget(self.toolbar)
        self.setLayout(layout)
