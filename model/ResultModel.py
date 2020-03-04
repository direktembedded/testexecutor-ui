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

class ResultModel(QAbstractListModel):

    NameRole = Qt.UserRole + 1
    ResultRole = Qt.UserRole + 2
    DurationRole = Qt.UserRole + 3
    NameKey = b'name'
    ResultKey = b'result'
    DurationKey = b'duration'

    def __init__(self, parent = None, clone = None):
        QAbstractListModel.__init__(self, parent)
        if clone:
            self._data = clone._data
        else:
            self._data = []

    def rowCount(self, index):
        return len(self._data)

    def roleNames(self):
        return {ResultModel.NameRole:ResultModel.NameKey,
                ResultModel.ResultRole:ResultModel.ResultKey,
                ResultModel.DurationRole:ResultModel.DurationKey}

    def data(self, index, role):
        d = self._data[index.row()]
        if role == ResultModel.NameRole:
            return d[ResultModel.NameKey]
        elif role == ResultModel.ResultRole:
            return d[ResultModel.ResultKey]
        elif role == ResultModel.DurationRole:
            return d[ResultModel.DurationKey]
        return None

    def populate(self):
        self._data.append({b'name':'test1', b'result':'feature one succeeded', b'duration':10})
        self._data.append({b'name':'test2', b'result':'feature two passed', b'duration':20})
        self._data.append({b'name':'test3', b'result':'feature three did not', b'duration':30})

    def populate2(self):
        self._data.append({b'name':'test3', b'result':'another test', b'duration':1})
        self._data.append({b'name':'test4', b'result':'to verify', b'duration':2})

    def add(self, name, result):
        rowCount = self.rowCount(QModelIndex())
        self.beginInsertRows(QModelIndex(), rowCount, rowCount)
        self._data.append({b'name':name, b'result':result, b'duration':None})
        self.endInsertRows()

    def changeme(self, name, result):
        row = 0 # pass this as argument
        ix = self.index(row, 0)
        self._data[row][b'result'] = result
        self.dataChanged.emit(ix, ix, self.roleNames())
        self.add(name, result)

