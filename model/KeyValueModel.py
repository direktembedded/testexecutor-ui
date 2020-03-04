"""
Copyright (c) 2020 Direkt, Australia
Licensed under BSD-3-Clause, refer LICENSE.txt
"""
# This Python file uses the following encoding: utf-8
from PySide2 import QtCore
from PySide2 import QtWidgets
from PySide2.QtCore import QAbstractListModel
from PySide2.QtCore import Qt
from PySide2.QtCore import QModelIndex
from PySide2.QtCore import QObject

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
        return {KeyValueModel.KeyRole:KeyValueModel.KeyKey, KeyValueModel.ValueRole:KeyValueModel.ValueKey}

    def data(self, index, role):
        d = self._data[index.row()]
        if role == KeyValueModel.KeyRole:
            return d[KeyValueModel.KeyKey]
        elif role == KeyValueModel.ValueRole:
            return d[KeyValueModel.ValueKey]
        return None

    def populate(self):
        self._data.append({b'key':'id1', b'value':'1234567890'})
        self._data.append({b'key':'id2', b'value':'Secondary id'})
        self._data.append({b'key':'another', b'value':'Id for reference'})
        self._data.append({b'key':'one', b'value':'908976543211234'})

    def populate2(self):
        self._data.append({b'key':'akey', b'value':'key one'})
        self._data.append({b'key':'bkey', b'value':'key two'})

    def add(self, key, value):
        rowCount = self.rowCount(QModelIndex())
        self.beginInsertRows(QModelIndex(), rowCount, rowCount)
        self._data.append({b'key':key, b'value':value})
        self.endInsertRows()

    def changeme(self, key, value):
        row = 0 # pass this as argument
        ix = self.index(row, 0)
        self._data[row][b'value'] = value
        self.dataChanged.emit(ix, ix, self.roleNames())
        self.add('test', value)

