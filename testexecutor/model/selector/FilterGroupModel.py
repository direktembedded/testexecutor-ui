#  Copyright 2020 Sipke Vriend, Australia
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
Model for a list of filters as FilterModel.
"""

from PySide6.QtCore import QAbstractListModel
from PySide6.QtCore import Qt
from PySide6.QtCore import QModelIndex
from .FilterModel import FilterModel


class FilterGroupModel(QAbstractListModel):

    FilterRole = Qt.UserRole
    FilterKey = b"filter"

    _roles = {
              FilterRole: FilterKey
             }

    def __init__(self, filters=None, parent=None, onSelectedChanged=None):
        QAbstractListModel.__init__(self, parent)
        self._datas = []
        if type(filters) == dict:
            for item in filters.items():
                filter = FilterModel(item[0], item[1])
                if onSelectedChanged:
                    filter.updated_selected.connect(onSelectedChanged, Qt.QueuedConnection)
                self.addData(filter)

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
        if role == self.FilterRole:
            self._datas[index.row()] = value
            self.dataChanged.emit(index, index, {self.FilterRole: self.FilterKey})
        return True

    def rowCount(self, parent=QModelIndex()):
        return len(self._datas)

    def data(self, index, role=Qt.DisplayRole):
        try:
            data = self._datas[index.row()]
        except IndexError:
            return None

        if role == self.FilterRole:
            return data

        return None

    def roleNames(self):
        return self._roles

    def updateData(self, name, content_list):
        """
        Update an existing filter with new content. If filter with name does not exist, nothing will happen
        :param name:
        :param content_list:
        :return:
        """
        rowCount = self.rowCount()
        for i in range(rowCount):
            existingItem = self.index(i, 0).data(self.FilterRole)
            if existingItem.name == name:
                existingItem.proposed.setStringList(content_list)
                self.dataChanged.emit(self.index(i, 0), self.index(i, 0), self._roles)
