"""
Copyright (c) 2020 Direkt, Australia
Licensed under BSD-3-Clause, refer LICENSE.txt
"""
# This Python file uses the following encoding: utf-8
from PySide2 import QtWidgets
from PySide2.QtCore import QAbstractListModel
from PySide2.QtCore import Qt
from PySide2.QtCore import QModelIndex
from PySide2.QtCore import QObject

class TestSuiteModel:
        def __init__(self, resultlist=None):
            self._resultlist = resultlist

        def resultlist(self):
            return self._resultlist

        def keyvalues(self):
            return None

        def instructions(self):
            return "None for instructions"


class TestSuiteGroup(QAbstractListModel):

    KeyValueListRole = Qt.UserRole + 1
    InstructionsRole = Qt.UserRole + 2
    ResultListRole = Qt.UserRole + 3
    KeyValueListKey = "keyvalues"
    InstructionsKey = "instructions"
    ResultListKey = "resultlist"

    _roles = {KeyValueListRole: b"keyvalues", InstructionsRole: b"instructions", ResultListRole: b"resultlist"}

    def __init__(self, parent=None):
        QAbstractListModel.__init__(self, parent)
        self._datas = []

    def addData(self, data):
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        self._datas.append(data)
        self.endInsertRows()

    def rowCount(self, parent=QModelIndex()):
        return len(self._datas)

    def data(self, index, role=Qt.DisplayRole):
        try:
            data = self._datas[index.row()]
        except IndexError:
            return QVariant()

        if role == self.KeyValueListRole:
            return data.keyvalues()

        if role == self.InstructionsRole:
            return data.instructions()

        if role == self.ResultListRole:
            return data.resultlist()

        return QVariant()

    def roleNames(self):
        return self._roles
