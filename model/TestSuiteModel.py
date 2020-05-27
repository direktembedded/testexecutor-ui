"""
Copyright (c) 2020 Direkt, Australia
Licensed under BSD-3-Clause, refer LICENSE
"""
# This Python file uses the following encoding: utf-8
import threading
from PySide2.QtCore import QObject
from PySide2.QtCore import Signal, Property, Slot
from model.InstructionsModel import InstructionModel

class TestSuiteModel(QObject):
    # these state strings must match those in TestSuiteWidget.qml
    STATE_RUNNING = "running"
    STATE_STARTING = "starting"
    STATE_STOPPING = "stopping"
    STATE_STOPPED = "stopped"
    STATE_END = "end"
    STATE_IDLE = "idle"
    STATE_READY = "ready"
    ACTION_CLEAR = "Clear"
    ACTION_STOP = "Stop"

    def __init__(self, idlist=None, resultlist=None, setid_callback=None, setstate_callback=None, title=None):
        QObject.__init__(self)
        self.lock = threading.RLock()
        self._setidentifiers(idlist)
        self._setresults(resultlist)
        self._setinstructions(InstructionModel())
        self._newId = None  # See newid Property below
        self.setid_callback = setid_callback
        self._state = None  # see suitestate Property below
        self.setstate_callback = setstate_callback
        self._title = title

    def clear(self):
        self.instructions.clear()
        self.results.clear()
        self.identifiers.clearData()
        self.suitestate = self.STATE_IDLE

    def setstate(self, st):
        """ Setter for suitestate Property """
        newstate = None
        changed = False
        if self.setstate_callback:
            newstate = self.setstate_callback(st)
        else:
            newstate = st
        with self.lock:
            if newstate and newstate != self._state:
                changed = True
            if changed:
                self._state = newstate
        if changed:
            if newstate == self.STATE_READY:
                self.results.clear()
            elif newstate == self.STATE_STOPPING:
                self.instructions.clear()
            self.result_changed.emit()
            self.stateChanged.emit()

    def _getstate(self):
        """ Getter for suitestate Property """
        state = None
        with self.lock:
            state = self._state
        return state

    stateChanged = Signal()
    suitestate = Property(str, _getstate, setstate, notify=stateChanged)

    def _setid(self, id):
        """ Setter for newid Property """
        with self.lock:
            self._newId = id
        if self.setid_callback:
            self.setid_callback(id)
        self.id_changed.emit()

    def _getid(self):
        """ Getter for newid Property """
        id = None
        with self.lock:
            id = self._newId
        return id

    id_changed = Signal()
    newid = Property(str, _getid, _setid, notify=id_changed)

    def _setidentifiers(self, identifiers):
        """ Setter for identifiers QAbstractList Property """
        with self.lock:
            self._idlist = identifiers
        self.identifiers_changed.emit()

    def _getidentifiers(self):
        """ Getter for identifiers QAbstractList Property """
        with self.lock:
            list = self._idlist
        return list

    identifiers_changed = Signal()
    identifiers = Property(QObject, _getidentifiers, _setidentifiers, notify=identifiers_changed)

    def _setresults(self, results):
        """ Setter for results QAbstractList Property """
        with self.lock:
            self._resultlist = results
        self.results_changed.emit()

    def _getresults(self):
        """ Getter for results QAbstractList Property """
        with self.lock:
            list = self._resultlist
        return list

    results_changed = Signal()
    results = Property(QObject, _getresults, _setresults, notify=results_changed)

    def _setinstructions(self, instruction_info):
        """ Setter for instructions Property """
        with self.lock:
            self._instructions = instruction_info
        self.instructions_changed.emit()

    def _getinstructions(self):
        """ Getter for instructions Property """
        with self.lock:
            instr = self._instructions
        return instr

    instructions_changed = Signal()
    instructions = Property(QObject, _getinstructions, _setinstructions, notify=instructions_changed)

    def _getresult(self):
        """
        Getter for result Property
        Checks all test results and returns state
        :return: Result.StatePass if every test passed
                 Result.StateFail if a single test failed within suite
                 Result.StateRunning if suite is still in progress
                 None if error occurred or no tests started
        """
        suite_result = None
        with self.lock:
            if self.results:
                suite_result = self.results.overallResult()
        return suite_result

    result_changed = Signal()
    result = Property(str, _getresult, None, notify=result_changed)

    def _settitle(self, title):
        """ Setter for title Property """
        changed = False
        with self.lock:
            if self._title != title:
                self._title = title
                changed = True
        if changed:
            self.title_changed.emit()

    def _gettitle(self):
        """ Getter for title Property """
        title = ""
        with self.lock:
            title = self._title
        return title

    title_changed = Signal()
    title = Property(str, _gettitle, _settitle, notify=title_changed)

    @Slot()
    def active(self):
        activeStates = [self.STATE_STOPPING, self.STATE_STARTING, self.STATE_RUNNING]
        return self.suitestate in activeStates

    @Slot(str)
    def action(self, action):
        """
        Two default actions are supported, Clear and Stop. The action string comes from the text on the control/action
        button of the TestSuiteWidget.qml states, so ensure the configuration has strings which match exactly.
        :param action:
        :return:
        """
        if action == self.ACTION_CLEAR:
            self.clear()
        elif action == self.ACTION_STOP:
            self.suitestate = self.STATE_STOPPING
