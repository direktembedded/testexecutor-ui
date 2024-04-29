#  Copyright 2020 Direkt, Australia
#  Copyright 2021 Direkt Embedded Pty Ltd
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

# This Python file uses the following encoding: utf-8
import threading
from PySide6 import QtCore
from PySide6.QtCore import QAbstractListModel
from PySide6.QtCore import Qt
from PySide6.QtCore import QModelIndex
from PySide6.QtCore import Slot
from PySide6.QtCore import Signal
from PySide6.QtCore import Property
from PySide6.QtCore import QObject

class Result(QObject):

    StateRunning = "Running"
    StatePass = "Pass"
    StateFail = "Fail"

    def __init__(self, name, result=None, feedback=None):
        QObject.__init__(self)
        self.lock = threading.RLock()
        self._name = name
        self._feedback = feedback
        self._result = result
        self._duration = 0
        self._progress = 0

    def _setfeedback(self, feedback):
        """ Setter for feedback Property """
        changed = False
        with self.lock:
            if self._feedback != feedback:
                self._feedback = feedback
                changed = True
        if changed:
            self.feedback_changed.emit()

    def _getfeedback(self):
        """ Getter for feedback Property """
        with self.lock:
            fb = self._feedback
        return fb

    feedback_changed = Signal()
    feedback = Property(str, _getfeedback, _setfeedback, notify=feedback_changed)

    def _setresult(self, result):
        """ Setter for result Property """
        changed = False
        with self.lock:
            if self._result != result:
                self._result = result
                changed = True
        if changed:
            self.result_changed.emit()

    def _getresult(self):
        """ Getter for result Property """
        with self.lock:
            r = self._result
        return r

    result_changed = Signal()
    result = Property(str, _getresult, _setresult, notify=result_changed)

    def _setduration(self, duration):
        """ Setter for duration Property """
        changed = False
        with self.lock:
            if self._duration != duration:
                self._duration = duration
                changed = True
        if changed:
            self.duration_changed.emit()

    def _getduration(self):
        """ Getter for duration Property """
        with self.lock:
            dur = self._duration
        return dur

    duration_changed = Signal()
    duration = Property(int, _getduration, _setduration, notify=duration_changed)

    def _setname(self, name):
        """ Setter for name Property """
        changed = False
        with self.lock:
            if self._name != name:
                self._name = name
                changed = True
        if changed:
            self.name_changed.emit()

    def _getname(self):
        """ Getter for name Property """
        with self.lock:
            n = self._name
        return n

    name_changed = Signal()
    name = Property(str, _getname, _setname, notify=name_changed)

    def _setprogress(self, progress):
        """ Setter for progress Property """
        changed = False
        with self.lock:
            if self._progress != progress:
                if progress > 1:
                    progress = 1
                elif progress < 0:
                    progress = 0
                self._progress = progress
                changed = True
        if changed:
            self.progress_changed.emit()

    def _getprogress(self):
        """ Getter for progress Property """
        return self._progress

    progress_changed = Signal()
    progress = Property(float, _getprogress, _setprogress, notify=progress_changed)


class ResultModel(QAbstractListModel):

    TestRole = Qt.UserRole
    TestKey = b"test"

    def __init__(self, parent=None):
        QAbstractListModel.__init__(self, parent)
        self.lock = threading.RLock()
        self._currentTestIndex = -1
        self._data = []

    def rowCount(self, parent=QModelIndex()):
        return len(self._data)

    def roleNames(self):
        return {self.TestRole: self.TestKey}

    def data(self, index, role=None):
        i = index.row()
        if len(self._data) > i:
            d = self._data[i]
            if role == self.TestRole:
                return d[self.TestKey]
        return None

    def setData(self, index, value, role=None):
        i = index.row()
        if len(self._data) > i:
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
    def add(self, name, result, feedback=None):
        rowCount = self.rowCount()
        self.beginInsertRows(QModelIndex(), rowCount, rowCount)
        test = {b'test': Result(name, result, feedback)}
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
                self._setcurrentTestIndex(row)
                self.dataChanged.emit(ix, ix, self.roleNames())
                existing = True
                break
        if not existing:
            self.add(name, Result.StateRunning)
            self._setcurrentTestIndex(len(self._data) - 1)

    @Slot(str, str)
    def end(self, name, result):
        """
        Method called to end a test.
        Only updated if test is found. If no tests with name exist, nothing is done.
        :param name: unique name of the test
        :param result: test result for the suite
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
            self.add(key, None, feedback)

    @Slot()
    def clear(self):
        rowCount = self.rowCount(QModelIndex())
        if rowCount:
            self.beginRemoveRows(QModelIndex(), 0, rowCount - 1)
            self._data.clear()
            self.endRemoveRows()

    @Slot(list, bool)
    def populateTests(self, tests, clear):
        if clear:
            self.removeRows(0, self.rowCount(QModelIndex()))
        if tests:
            for test in tests:
                self.add(test, None)

    def removeRows(self, position, rows, parent=QtCore.QModelIndex()):
        self.beginRemoveRows(parent, position, position + rows - 1)
        del self._data[position:position + rows]
        self.endRemoveRows()
        return True

    def _setcurrentTestIndex(self, currentTestIndex):
        """ Setter for currentTestIndex Property """
        changed = False
        with self.lock:
            if self._currentTestIndex != currentTestIndex:
                self._currentTestIndex = currentTestIndex
                changed = True
        if changed:
            self.currentTestIndex_changed.emit()

    def _getcurrentTestIndex(self):
        """ Getter for currentTestIndex Property """
        with self.lock:
            index = self._currentTestIndex
        return index

    currentTestIndex_changed = Signal()
    currentTestIndex = Property(int, _getcurrentTestIndex, _setcurrentTestIndex, notify=currentTestIndex_changed)
