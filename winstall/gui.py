import asyncio
import sys

from asyncqt import QEventLoop
from PyQt5 import QtCore, QtGui, QtWidgets

from packages import *


class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data=None):
        super(TableModel, self).__init__()
        if data is None:
            data = []
        self._data = data

    def data(self, index, role=QtCore.Qt.DisplayRole):
        # if role == QtCore.Qt.DisplayRole and 0 <= index.row() < self.rowCount() and 0 <= index.column() < self.columnCount():
        #     return self._data[index.row()][index.column()]
        if role == QtCore.Qt.DisplayRole and 0 <= index.row() < self.rowCount() and 0 <= index.column() < self.columnCount():
            value = self._data[index.row()][index.column()]
            if isinstance(value, bool):
                if value:
                    return "✅"
                return "🛑"
            return value

    def setData(self, index, value, role=QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole and 0 <= index.row() < self.rowCount() and 0 <= index.column() < self.columnCount():
            self._data[index.row()][index.column()] = value
            self.dataChanged.emit(index, index, (role,))

    def rowCount(self, index=QtCore.QModelIndex()):
        try:
            return len(self._data)
        except:
            return 0

    def columnCount(self, index=QtCore.QModelIndex()):
        try:
            return len(self._data[0])
        except:
            return 0

    def set_data(self, data):
        self.beginResetModel()
        self._data = data
        self.endResetModel()


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.resize(700, 400)
        self.centralWidget()
        self.setWindowTitle("Winstall")

        self.table = QtWidgets.QTableView()
        self.table.verticalHeader().hide()
        self.table.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)

        self.model = TableModel()
        self.table.setModel(self.model)
        self.setCentralWidget(self.table)

        asyncio.ensure_future(self.fill_model())

    async def fill_model(self):
        data = []
        items = [AndroidSdkCmdlineTools(), Antidote()]
        data = [[False, item.package_name, item.package_type, item.is_installed, "♾️", item.package_info] for item in items]
        self.model.set_data(data)
        await asyncio.gather(*(self.update_row(row, item) for row, item in enumerate(items)))

    async def update_row(self, row, item):
        value = await item.needs_update
        index = self.model.index(row, 4)
        self.model.setData(index, value)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)
    window = MainWindow()
    window.show()
    with loop:
        loop.run_forever()
