"""
Copyright (c) 2020 Direkt, Australia
Licensed under BSD-3-Clause, refer LICENSE
"""
# This Python file uses the following encoding: utf-8
from PySide2.QtCore import QAbstractListModel
from PySide2.QtCore import Qt
from PySide2.QtCore import QObject
from PySide2.QtCore import QModelIndex
from PySide2.QtCore import Property, Signal


class KeyValueModel(QAbstractListModel):

    KeyRole = Qt.UserRole + 1
    LabelRole = Qt.UserRole + 2
    ValueRole = Qt.UserRole + 3
    KeyKey = b'key'
    LabelKey = b'label'
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
        return {KeyValueModel.KeyRole: KeyValueModel.KeyKey,
                KeyValueModel.LabelRole: KeyValueModel.LabelKey,
                KeyValueModel.ValueRole: KeyValueModel.ValueKey}

    def data(self, index, role):
        d = self._data[index.row()]
        if role == KeyValueModel.KeyRole:
            return d[KeyValueModel.KeyKey]
        elif role == KeyValueModel.LabelRole:
            return d[KeyValueModel.LabelKey]
        elif role == KeyValueModel.ValueRole:
            return d[KeyValueModel.ValueKey]
        return None

    def add(self, key, value, label=None):
        if not label:
            label = key
        if type(value) is not list:
            value = [value]
        rowCount = self.rowCount(QModelIndex())
        self.beginInsertRows(QModelIndex(), rowCount, rowCount)
        self._data.append({KeyValueModel.KeyKey: key, KeyValueModel.ValueKey: value, KeyValueModel.LabelKey: label})
        self.endInsertRows()

    def setData(self, index, value, role=None):
        self._data[index.row()] = value
        self.dataChanged.emit(index, index, self.roleNames())

    def setValue(self, key, value):
        if type(value) is not list:
            value = [value]
        for row in range(len(self._data)):
            if self._data[row][KeyValueModel.KeyKey] == key:
                self._data[row][KeyValueModel.ValueKey] = value
                ix = self.index(row, 0)
                self.dataChanged.emit(ix, ix, self.roleNames())
                break

    def getValue(self, key):
        value = None
        for row in range(len(self._data)):
            if self._data[row][KeyValueModel.KeyKey] == key:
                value = self._data[row][KeyValueModel.ValueKey]
        return value

    def clearData(self):
        for row in range(len(self._data)):
            self._data[row][KeyValueModel.ValueKey] = ""
            ix = self.index(row, 0)
            self.dataChanged.emit(ix, ix, self.roleNames())
