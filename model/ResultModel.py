"""
Copyright (c) 2020 Direkt, Australia
Licensed under BSD-3-Clause, refer LICENSE.txt
"""
# This Python file uses the following encoding: utf-8
from PySide2 import QtCore
from PySide2.QtCore import QAbstractListModel
from PySide2.QtCore import Qt
from PySide2.QtCore import QModelIndex
from PySide2.QtCore import Slot
from PySide2.QtCore import Signal
from PySide2.QtCore import Property
from PySide2.QtCore import QObject

class Result(QObject):
    def __init__(self, name):
        QObject.__init__(self)
        #self._setidentifiers(idlist)
        self._name = name
        self._feedback = None
        self._result = None
        self._duration = None

    def _setfeedback(self, feedback):
        """ Setter for feedback Property """
        if self._feedback != feedback:
            self._feedback = feedback
            self.feedback_changed.emit()

    def _getfeedback(self):
        """ Getter for feedback Property """
        return self._feedback

    feedback_changed = Signal()
    feedback = Property(str, _getfeedback, _setfeedback, notify=feedback_changed)

    def _setresult(self, result):
        """ Setter for result Property """
        if self._result != result:
            self._result = result
            self.result_changed.emit()

    def _getresult(self):
        """ Getter for result Property """
        return self._result

    result_changed = Signal()
    result = Property(str, _getresult, _setresult, notify=result_changed)

    def _setduration(self, duration):
        """ Setter for duration Property """
        if self._duration != duration:
            self._duration = duration
            self.duration_changed.emit()

    def _getduration(self):
        """ Getter for duration Property """
        return self._duration

    duration_changed = Signal()
    duration = Property(str, _getduration, _setduration, notify=duration_changed)

    def _setname(self, name):
        """ Setter for name Property """
        if self._name != name:
            self._name = name
            self.name_changed.emit()

    def _getname(self):
        """ Getter for name Property """
        return self._name

    name_changed = Signal()
    name = Property(str, _getname, _setname, notify=name_changed)



class ResultModel(QAbstractListModel):

    TestRole = Qt.UserRole
    NameRole = Qt.UserRole + 1
    ResultRole = Qt.UserRole + 2
    DurationRole = Qt.UserRole + 3
    NameKey = b'name'
    ResultKey = b'result'
    DurationKey = b'duration'
    TestKey = b'test'

    def __init__(self, parent=None, clone=None):
        QAbstractListModel.__init__(self, parent)
        if clone:
            self._data = clone._data
        else:
            self._data = []

    def rowCount(self, parent=QModelIndex()):
        return len(self._data)

    def roleNames(self):
        return {self.TestRole: self.TestKey,
                ResultModel.NameRole:ResultModel.NameKey,
                ResultModel.ResultRole:ResultModel.ResultKey,
                ResultModel.DurationRole:ResultModel.DurationKey}

    def data(self, index, role):
        d = self._data[index.row()]
        if role == self.TestRole:
            return d[self.TestKey]
        elif role == ResultModel.NameRole:
            return d[ResultModel.NameKey]
        elif role == ResultModel.ResultRole:
            return d[ResultModel.ResultKey]
        elif role == ResultModel.DurationRole:
            return d[ResultModel.DurationKey]
        return None

    def setData(self, index, value, role=None):
        print("result setData", index.row(), value, role)
        self._data[index.row()] = value
        self.dataChanged.emit(index, index, self.roleNames())

    @Slot(str, str)
    def add(self, name, result):
        rowCount = self.rowCount()
        self.beginInsertRows(QModelIndex(), rowCount, rowCount)
        test = {b'name': name, b'result': result, b'duration': None, b'test': Result(name)}
        self._data.append(test)
        self.endInsertRows()
        return test

    @Slot(str)
    def start(self, name):
        existing = False
        for row in range(len(self._data)):
            test = self._data[row]
            if test[self.NameKey] == name:
                print("start", name)
                ix = self.index(row, 0)
                self.dataChanged.emit(ix, ix, self.roleNames())
                existing = True
                break
        if not existing:
            self.add(name, None)

    @Slot(str, str)
    def setFeedback(self, key, feedback):
        existing = False
        for row in range(len(self._data)):
            if self._data[row][self.NameKey] == key:
                test = self._data[row][self.TestKey]
                test.feedback = feedback
                ix = self.index(row, 0)
                self.dataChanged.emit(ix, ix, self.roleNames())
                existing = True
                break
        if not existing:
            test = self.add(key, None)
            test.feedback = feedback

    @Slot()
    def clear(self):
        rowCount = self.rowCount(QModelIndex())
        if rowCount:
            self.beginRemoveRows(QModelIndex(), 0, rowCount - 1)
            self._data.clear()
            self.endRemoveRows()

    @Slot(list)
    def populateTests(self, tests):
        if not self.removeRows(0, self.rowCount(QModelIndex())):
            print("FAILED to remove rows")
        if tests:
            for test in tests:
                self.add(test, None)

    def removeRows(self, position, rows, parent=QtCore.QModelIndex()):
        self.beginRemoveRows(parent, position, position + rows - 1)
        self._data.clear()
        self.endRemoveRows()
        return True
