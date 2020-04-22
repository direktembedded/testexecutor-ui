"""
Copyright (c) 2020 Direkt, Australia
Licensed under BSD-3-Clause, refer LICENSE
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

    StateRunning = "Running"
    StatePass = "Pass"
    StateFail = "Fail"

    def __init__(self, name):
        QObject.__init__(self)
        #self._setidentifiers(idlist)
        self._name = name
        self._feedback = None
        self._result = None
        self._duration = None
        self._progress = 0

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

    def _setprogress(self, progress):
        """ Setter for progress Property """
        if self._progress != progress:
            if progress > 1:
                progress = 1
            elif progress < 0:
                progress = 0
            self._progress = progress
            self.progress_changed.emit()

    def _getprogress(self):
        """ Getter for progress Property """
        return self._progress

    progress_changed = Signal()
    progress = Property(float, _getprogress, _setprogress, notify=progress_changed)


class ResultModel(QAbstractListModel):

    TestRole = Qt.UserRole
    TestKey = b"test"

    def __init__(self, parent=None, clone=None):
        QAbstractListModel.__init__(self, parent)
        if clone:
            self._data = clone._data
        else:
            self._data = []

    def rowCount(self, parent=QModelIndex()):
        return len(self._data)

    def roleNames(self):
        return {self.TestRole: self.TestKey}

    def data(self, index, role):
        d = self._data[index.row()]
        if role == self.TestRole:
            return d[self.TestKey]
        return None

    def setData(self, index, value, role=None):
        self._data[index.row()] = value
        self.dataChanged.emit(index, index, self.roleNames())

    def overallResult(self):
        """
        Return the test suite result status
        :return: None: State is unknown. Either no test results or error occurred.
                 Result.StateRunning: A test is in progress
                 Result.StatePass: All test have been run and all passed
                 Result.StateFail: One state failed
        """
        overall_result = None
        passed_count = 0
        if self._data and len(self._data):
            for item in self._data:
                test = item[self.TestKey]
                if test.result == Result.StateFail:
                    overall_result = test.result
                    break
                elif test.result == Result.StateRunning:
                    overall_result = test.result
                    break
            if not overall_result:
                overall_result = Result.StatePass
        return overall_result


    @Slot(str, str)
    def add(self, name, result):
        rowCount = self.rowCount()
        self.beginInsertRows(QModelIndex(), rowCount, rowCount)
        test = {b'test': Result(name)}
        self._data.append(test)
        self.endInsertRows()
        return test

    @Slot(str)
    def start(self, name):
        """
        Method called to either add a new test, or re-start an existing one.
        If the name-d test is found its 'content' will be cleared and restarted.
        If it is not found the test will be added to the list and executed.
        :param name: unique name of the test
        :return: None
        """
        existing = False
        for row in range(len(self._data)):
            test = self._data[row][self.TestKey]
            if test.name == name:
                test.result = Result.StateRunning
                ix = self.index(row, 0)
                self.dataChanged.emit(ix, ix, self.roleNames())
                existing = True
                break
        if not existing:
            self.add(name, None)

    @Slot(str, str)
    def end(self, name, result):
        """
        Method called to end a test.
        Only updated if test is found. If no tests with name exist, nothing is done.
        :param name: unique name of the test
        :return: None
        """
        for row in range(len(self._data)):
            test = self._data[row][self.TestKey]
            if test.name == name:
                test.result = result
                test.progress = 1
                ix = self.index(row, 0)
                self.dataChanged.emit(ix, ix, self.roleNames())
                break

    @Slot(str, int)
    def progress(self, name, progress):
        """
        Method called to end a test.
        Only updated if test is found. If no tests with name exist, nothing is done.
        :param name: unique name of the test
        :param progress: 0 to 100 for percentage of test progress.
        :return: None
        """
        for row in range(len(self._data)):
            test = self._data[row][self.TestKey]
            if test.name == name:
                test.progress = progress / 100
                ix = self.index(row, 0)
                self.dataChanged.emit(ix, ix, self.roleNames())
                break

    @Slot(str, str)
    def setFeedback(self, key, feedback):
        existing = False
        for row in range(len(self._data)):
            test = self._data[row][self.TestKey]
            if test.name == key:
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
