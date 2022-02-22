#  Copyright 2020 Direkt, Australia
#  Copyright 2021 Direkt Embedded Pty Ltd
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

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
"""

from PySide6.QtCore import QAbstractListModel
from PySide6.QtCore import Qt
from PySide6.QtCore import QModelIndex
from PySide6.QtCore import Signal, Property


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

    def setData(self, index, value, role=None):
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
            return None

        if role == self.TestSuiteRole:
            return data

        return None

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

    def abortAll(self, hard=False):
        for item in self._datas:
            if hard:
                item.close()
            else:
                item.suitestate = "stopping"
