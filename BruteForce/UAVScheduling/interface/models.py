from PySide2.QtCore import QAbstractTableModel, Qt, QModelIndex

from dwta import models


class TargetsModel(QAbstractTableModel):
    # TODO: добавить правильное изменение Target.value

    # see: https://stackoverflow.com/q/48622778/10380652

    HEADERS = ['id', 'position', 'value']

    def __init__(self, world, parent=None):
        super().__init__(parent)

        # по сути, в терминах C++, это ссылка на данные, которые мы отображаем
        # (конкретно в этом случае, мы ссылаемся на actor'ов класса World)
        self.world = world

        self.world.sigActorAdded.connect(self.add_target)
        self.world.sigActorRemoved.connect(self.remove_target)

        # в C++ для этих целей можно было использовать указатель на underlying
        # data. также можно хранить внутри модели дубликат объектов
        # self.targets = []

    # def set_targets(self, targets):
    #     """Completely update model data."""
    #     self.beginResetModel()
    #     self.targets = targets
    #     self.endResetModel()

    # NOTE: На эти методы навешиваются сигналы, чтобы все отображения (views)
    #  правильно отрисовывались. в них самый цимес, когда данные хранятся не
    #  в модели (в терминах MVC)
    def add_target(self, target):
        if not isinstance(target, models.Target):
            return False

        # see: https://stackoverflow.com/a/30776237/10380652
        row = len(self.targets)
        self.beginInsertRows(QModelIndex(), row, row)
        # self.targets.append(target)
        self.endInsertRows()

    def remove_target(self, target):
        if not isinstance(target, models.Target):
            return False

        # see: https://stackoverflow.com/a/30776237/10380652
        row = len(self.targets)
        self.beginRemoveRows(QModelIndex(), row, row)
        # self.targets.append(target)
        self.endRemoveRows()

    @property
    def targets(self):
        return self.world.get_actors(models.Target)

    def rowCount(self, parent_index):
        return len(self.targets)

    def columnCount(self, parent_index):
        return len(self.HEADERS)

    def data(self, index, role):
        """Defines what do you print in the cells."""
        if not index.isValid():
            return None

        if role == Qt.DisplayRole:
            row = index.row()
            column = index.column()
            target = self.targets[row]

            if column == 0:
                return str(target.id)

            if column == 1:
                return str(target.position)

            if column == 2:
                return str(target.value)

        return None

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self.HEADERS[section]

        return None

    def setData(self, index, value, role):
        if not index.isValid():
            return False

        if role == Qt.EditRole:
            row = index.row()
            column = index.column()
            target = self.targets[row]

            if column == 2:
                target.value = value

            self.dataChanged.emit(index, index)

        return True

    def flags(self, index):
        original_flags = super().flags(index)
        flags = original_flags | Qt.ItemIsSelectable | Qt.ItemIsEnabled
        if index.column() == 2:
            flags |= Qt.ItemIsEditable
        return flags
