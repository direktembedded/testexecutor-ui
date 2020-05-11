"""
A class which inherits QAbstractListModel to provide a list of TestSuites for a multi test runner.
Usage
# Write your MyTestSuiteListener class which inherits TestSuiteListener and provide your business logic in the callbacks
# Setup the list of suites
mySuiteGroup = TestSuiteGroup()
for i in range(4):
    mySuiteGroup.addData(MyTestSuiteListener())

# Setup the qml UI
qml_file = os.path.join(ui_path, 'MultiTestWidget.qml')
url = QUrl.fromLocalFile(qml_file)
view.setSource(url)
view.setResizeMode(QQuickView.SizeRootObjectToView)
if view.status() != QQuickView.Error:
    # Set the UIs Property model_list to the set of 4 TestSuiteListeners (which inherit TestSuiteModel)
    view.rootContext().setContextProperty("model_list", mySuiteGroup)
    view.showMaximized()

Copyright (c) 2020 Direkt, Australia
Licensed under BSD-3-Clause, refer LICENSE
"""

from PySide2.QtCore import QAbstractListModel
from PySide2.QtCore import Qt
from PySide2.QtCore import QModelIndex
from PySide2.QtCore import Signal, Property


class TestSuiteGroup(QAbstractListModel):

    TestSuiteRole = Qt.UserRole
    TestSuiteKey = b"testsuite"

    _roles = {
              TestSuiteRole: TestSuiteKey
             }

    def __init__(self, parent=None):
        QAbstractListModel.__init__(self, parent)
        self._datas = []

    def addData(self, data):
        index = QModelIndex()
        self.beginInsertRows(index, self.rowCount(), self.rowCount())
        self._datas.append(data)
        self.endInsertRows()

    def setData(self, index, value, role):
        try:
            data = self._datas[index.row()]
        except IndexError:
            return False
        if role == self.TestSuiteRole:
            self._datas[index.row()] = value
            self.dataChanged.emit(index, index, {self.TestSuiteRole: self.TestSuiteKey})
        return True

    def rowCount(self, parent=QModelIndex()):
        return len(self._datas)

    def data(self, index, role=Qt.DisplayRole):
        try:
            data = self._datas[index.row()]
        except IndexError:
            return QVariant()

        if role == self.TestSuiteRole:
            return data

        return QVariant()

    def roleNames(self):
        return self._roles

    def _getactive_suites(self):
        """ Getter for active_suites Property """
        active = False
        for item in self._datas:
            active = item.active()
            if active:
                break
        return active

    active_suites_changed = Signal()
    active_suites = Property(bool, _getactive_suites, None, notify=active_suites_changed)
