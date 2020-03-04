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
from PySide2.QtCore import Slot, Signal, Property

class TestSuiteModel(QObject):
    def __init__(self, resultlist=None, setid_callback=None):
        QObject.__init__(self)
        self._resultlist = resultlist
        self._newId = None
        self.setid_callback = setid_callback

    def resultlist(self):
        return self._resultlist

    def keyvalues(self):
        return None

    def instructions(self):
        return "None for instructions"

    def _setid(self, id):
        self._newId = id
        if self.setid_callback:
            self.setid_callback(id)

    def _getid(self):
        return self._newId

    @Signal
    def id_changed(self):
        pass

    newid = Property(str, _getid, _setid, notify=id_changed)


class TestSuiteGroup(QAbstractListModel):

    KeyValueListRole = Qt.UserRole + 1
    InstructionsRole = Qt.UserRole + 2
    ResultListRole = Qt.UserRole + 3
    NewIdRole = Qt.UserRole + 4
    KeyValueListKey = "keyvalues"
    InstructionsKey = "instructions"
    ResultListKey = "resultlist"
    NewIdKey = b"newid"

    _roles = {KeyValueListRole: b"keyvalues",
              InstructionsRole: b"instructions",
              ResultListRole: b"resultlist",
              NewIdRole: NewIdKey
              }

    def __init__(self, parent=None):
        QAbstractListModel.__init__(self, parent)
        self._datas = []

    def addData(self, data):
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        self._datas.append(data)
        self.endInsertRows()

    def setData(self, index, value, role):
        try:
            data = self._datas[index.row()]
        except IndexError:
            return False

        if role == self.NewIdRole:
            data.newid = value
        return True

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

        if role == self.NewIdRole:
            return data.newid

        return QVariant()

    def roleNames(self):
        return self._roles
