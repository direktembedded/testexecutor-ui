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

from model.SuiteStateModel import SuiteStateModel

class TestSuiteModel(QObject):
    # these state strings must match those in TestSuiteWidget.qml
    STATE_RUNNING = "running"
    STATE_STARTING = "starting"
    STATE_STOPPING = "stopping"
    STATE_STOPPED = "stopped"
    STATE_IDLE = "idle"
    STATE_READY = "ready"
    STATE_NEXT = "next"  # When suitestate is set to 'next', the UI state button has been pressed

    def __init__(self, idlist=None, resultlist=None, setid_callback=None, setstate_callback=None):
        QObject.__init__(self)
        self._idlist = idlist
        self._resultlist = resultlist
        self._newId = None  # See newid Property below
        self.setid_callback = setid_callback
        self._state = None  # see suitestate Property below
        self.setstate_callback = setstate_callback
        self.stateChanged.connect(self.weChangedState)

    @Slot()
    def weChangedState(self):
        pass

    def resultlist(self):
        return self._resultlist

    def keyvalues(self):
        return self._idlist

    def instructions(self):
        return "None for instructions"

    def _default_state_change(self, st):
        newstate = st
        if st == TestSuiteModel.STATE_NEXT:
            if newstate == TestSuiteModel.STATE_IDLE or not self._state:
                newstate = TestSuiteModel.STATE_RUNNING
            else:
                newstate = TestSuiteModel.STATE_IDLE
        return newstate

    def setstate(self, st):
        """ Setter for suitestate Property """
        newstate = None
        if self.setstate_callback:
            newstate = self.setstate_callback(st)
        if not newstate:
            newstate = self._default_state_change(st)
        if newstate != self._state:
            self._state = newstate
            self.stateChanged.emit()

    def _getstate(self):
        """ Getter for suitestate Property """
        return self._state

    stateChanged = Signal()
    suitestate = Property(str, _getstate, setstate, notify=stateChanged)

    def _setid(self, id):
        """ Setter for newid Property """
        self._newId = id
        if self.setid_callback:
            self.setid_callback(id)
        self.id_changed.emit()

    def _getid(self):
        """ Getter for newid Property """
        return self._newId

    id_changed = Signal()
    newid = Property(str, _getid, _setid, notify=id_changed)


class TestSuiteGroup(QAbstractListModel):

    IdentifierListRole = Qt.UserRole + 1
    InstructionsRole = Qt.UserRole + 2
    ResultListRole = Qt.UserRole + 3
    NewIdRole = Qt.UserRole + 4
    SuiteStateRole = Qt.UserRole + 5
    IdentifierListKey = b"identifiers"
    InstructionsKey = b"instructions"
    ResultListKey = b"resultlist"
    NewIdKey = b"newid"
    SuiteStateKey = b"suitestate"


    _roles = {IdentifierListRole: IdentifierListKey,
              InstructionsRole: InstructionsKey,
              ResultListRole: ResultListKey,
              NewIdRole: NewIdKey,
              SuiteStateRole: SuiteStateKey
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
            self.dataChanged.emit(index, index, {TestSuiteGroup.NewIdRole: TestSuiteGroup.NewIdKey})
        elif role == self.SuiteStateRole:
            data.suitestate = value
            self.dataChanged.emit(index, index, {TestSuiteGroup.SuiteStateRole: TestSuiteGroup.SuiteStateKey})
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

        if role == self.SuiteStateRole:
            return data.suitestate

        return QVariant()

    def roleNames(self):
        return self._roles

