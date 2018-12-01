import xml.etree.ElementTree as xml
from io import StringIO

from pyside2uic import compileUi
from PySide2 import QtWidgets  # this needed for loadUiType
from PySide2.QtGui import QMatrix
# from PySide2.QtUiTools import QUiLoader
# from PySide2.QtCore import Qt, QFile


def loadUiType(ui_file):
    """
    PySide lacks a "loadUiType" command like PyQt4's, so we have to convert
    the ui file to py code in-memory first and then execute it in a
    special frame to retrieve the form_class.

    from stackoverflow: http://stackoverflow.com/a/14195313/3781327
    """
    parsed = xml.parse(ui_file)
    form_class = parsed.find('class').text
    widget_class = parsed.find('widget').get('class')

    with open(ui_file, 'r') as f:
        o = StringIO()
        frame = {}

        compileUi(f, o, indent=0)
        pyc = compile(o.getvalue(), '<string>', 'exec')
        exec(pyc, frame)

        # Fetch the base_class and form class based on their type in the xml
        # from designer
        form_class = frame[f'Ui_{form_class}']
        base_class = eval(f'QtWidgets.{widget_class}')

    return form_class, base_class


# def loadMainWindow():
#     ui_filename = 'interface/mainwindow.ui'
#
#     ui_file = QFile(ui_filename)
#     ui_file.open(QFile.ReadOnly)
#
#     loader = QUiLoader()
#     loader.registerCustomWidget(MyView)
#     # loader.addPluginPath('interface')
#
#     ui = loader.load(ui_file, None)
#     ui_file.close()
#     return ui


def stable_matrix(matrix, point):
    # see: https://stackoverflow.com/a/40705307/10380652

    # Make sure we have a copy.
    new_matrix = QMatrix(matrix)

    scale_x = new_matrix.m11()
    scale_y = new_matrix.m22()
    new_matrix.scale(1.0 / scale_x, 1.0 / scale_y)

    offset_x = point.x() * (scale_x - 1.0)
    offset_y = point.y() * (scale_y - 1.0)
    new_matrix.translate(offset_x, offset_y)

    return new_matrix
