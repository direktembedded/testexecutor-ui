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
A QAbstractListModel with a single user role for a variant object, which should be given properties.
These properties can be accessed within qml models through model.item.<property_name>
"""

import threading
from PySide6.QtCore import QAbstractListModel
from PySide6.QtCore import Qt
from PySide6.QtCore import QModelIndex


class GenericListModel(QAbstractListModel):

    SelectionRole = Qt.UserRole
    NameKey = b"model"

    def __init__(self, parent=None):
        QAbstractListModel.__init__(self, parent)
        self.lock = threading.RLock()
        self._currentTestIndex = -1
        self._data = []

    def rowCount(self, parent=QModelIndex()):
        return len(self._data)

    def roleNames(self):
        return {self.SelectionRole: self.NameKey}

    def data(self, index, role=None):
        d = self._data[index.row()]
        if role == self.SelectionRole:
            return d
        return d

    def setData(self, index, value, role=None):
        self._data[index.row()] = value
        self.dataChanged.emit(index, index, self.roleNames())

    def add(self, item):
        rowCount = self.rowCount()
        self.beginInsertRows(QModelIndex(), rowCount, rowCount)
        self._data.append(item)
        self.endInsertRows()
        return item

    def clear(self):
        self.beginRemoveRows(QModelIndex(), 0, self.rowCount(QModelIndex()))
        self._data.clear()
        self.endRemoveRows()
