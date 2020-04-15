"""
Copyright (c) 2020 Direkt, Australia
Licensed under BSD-3-Clause, refer LICENSE.txt
"""
# This Python file uses the following encoding: utf-8
from PySide2.QtCore import QAbstractListModel
from PySide2.QtCore import Qt
from PySide2.QtCore import QModelIndex

class value:
    def __init__(self, key, value):
        key = key
        value = value

class KeyValueModel(QAbstractListModel):

    KeyRole = Qt.UserRole + 1
    ValueRole = Qt.UserRole + 2
    KeyKey = b'key'
    ValueKey = b'value'

    def __init__(self, parent = None, clone = None):
        QAbstractListModel.__init__(self, parent)
        if clone:
            self._data = clone._data
        else:
            self._data = []

    def rowCount(self, index):
        return len(self._data)

    def roleNames(self):
        return {KeyValueModel.KeyRole: KeyValueModel.KeyKey, KeyValueModel.ValueRole: KeyValueModel.ValueKey}

    def data(self, index, role):
        d = self._data[index.row()]
        if role == KeyValueModel.KeyRole:
            return d[KeyValueModel.KeyKey]
        elif role == KeyValueModel.ValueRole:
            return d[KeyValueModel.ValueKey]
        return None

    def add(self, key, value):
        rowCount = self.rowCount(QModelIndex())
        self.beginInsertRows(QModelIndex(), rowCount, rowCount)
        self._data.append({KeyValueModel.KeyKey: key, KeyValueModel.ValueKey: value})
        self.endInsertRows()

    def setData(self, index, value, role=None):
        self._data[index.row()] = value
        self.dataChanged.emit(index, index, self.roleNames())

    def setValue(self, key, value):
        for row in range(len(self._data)):
            if self._data[row][KeyValueModel.KeyKey] == key:
                self._data[row][KeyValueModel.ValueKey] = value
                ix = self.index(row, 0)
                self.dataChanged.emit(ix, ix, self.roleNames())
                break
