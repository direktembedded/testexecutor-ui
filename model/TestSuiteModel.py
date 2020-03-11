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
    def __init__(self, idlist=None, resultlist=None, setid_callback=None):
        QObject.__init__(self)
        self._idlist = idlist
        self._resultlist = resultlist
        self._newId = None # See newid Property below
        self.setid_callback = setid_callback

    def resultlist(self):
        return self._resultlist

    def keyvalues(self):
        return self._idlist

    def instructions(self):
        return "None for instructions"

    def _setid(self, id):
        """ Setter for newid Property """
        self._newId = id
        if self.setid_callback:
            self.setid_callback(id)

    def _getid(self):
        """ Getter for newid Property """
        return self._newId

    @Signal
    def id_changed(self):
        pass

    newid = Property(str, _getid, _setid, notify=id_changed)


class TestSuiteGroup(QAbstractListModel):

    IdentifierListRole = Qt.UserRole + 1
    InstructionsRole = Qt.UserRole + 2
    ResultListRole = Qt.UserRole + 3
    NewIdRole = Qt.UserRole + 4
    IdentifierListKey = b"identifiers"
    InstructionsKey = b"instructions"
    ResultListKey = b"resultlist"
    NewIdKey = b"newid"

    _roles = {IdentifierListRole: IdentifierListKey,
              InstructionsRole: InstructionsKey,
              ResultListRole: ResultListKey,
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

        if role == self.IdentifierListRole:
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
