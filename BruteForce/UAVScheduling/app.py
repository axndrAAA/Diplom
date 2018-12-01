import logging

from PySide2.QtWidgets import QApplication
from PySide2.QtCore import QRectF, Qt, QCoreApplication

from UAVScheduling.experiment.experiment import Experiment
from UAVScheduling.interface.main_window import MainWindow
from UAVScheduling.experiment.world import World, WorldArea

logging.basicConfig(level=logging.INFO)


def main():
    # Qt WebEngine seems to be initialized from a plugin. Please set
    # Qt::AA_ShareOpenGLContexts using QCoreApplication::setAttribute
    # before constructing QGuiApplication
    QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)

    # You should always create an QApplication instance before trying to use
    # GUI objects/widgets
    app = QApplication([])

    world = World(area=WorldArea(QRectF(0, 0, 2000, 2000)))
    experiment = Experiment(world)
    main_window = MainWindow(experiment)
    main_window.show()

    app.exec_()


if __name__ == '__main__':
    exit(main())
