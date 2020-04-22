"""
Copyright (c) 2020 Direkt, Australia
Licensed under BSD-3-Clause, refer LICENSE
"""
# This Python file uses the following encoding: utf-8
import threading
from PySide2.QtCore import QObject
from PySide2.QtCore import Signal, Property
from model.InstructionsModel import InstructionModel

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
        self._setidentifiers(idlist)
        self._setresults(resultlist)
        self._setinstructions(InstructionModel())
        self._newId = None  # See newid Property below
        self.setid_callback = setid_callback
        self._state = None  # see suitestate Property below
        self.setstate_callback = setstate_callback
        self.lock = threading.RLock()

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
        changed = False
        if self.setstate_callback:
            newstate = self.setstate_callback(st)
        else:
            newstate = self._default_state_change(st)
        with self.lock:
            if newstate and newstate != self._state:
                changed = True
            if changed:
                self._state = newstate
        if changed:
            if self._state == self.STATE_READY:
                self.results.clear()
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
        self._newId = id
        if self.setid_callback:
            self.setid_callback(id)
        self.id_changed.emit()

    def _getid(self):
        """ Getter for newid Property """
        return self._newId

    id_changed = Signal()
    newid = Property(str, _getid, _setid, notify=id_changed)

    def _setidentifiers(self, identifiers):
        """ Setter for identifiers QAbstractList Property """
        self._idlist = identifiers
        self.identifiers_changed.emit()

    def _getidentifiers(self):
        """ Getter for identifiers QAbstractList Property """
        return self._idlist

    identifiers_changed = Signal()
    identifiers = Property(QObject, _getidentifiers, _setidentifiers, notify=identifiers_changed)

    def _setresults(self, results):
        """ Setter for results QAbstractList Property """
        self._resultlist = results
        self.results_changed.emit()

    def _getresults(self):
        """ Getter for results QAbstractList Property """
        return self._resultlist

    results_changed = Signal()
    results = Property(QObject, _getresults, _setresults, notify=results_changed)

    def _setinstructions(self, instruction_info):
        """ Setter for instructions Property """
        self._instructions = instruction_info
        self.instructions_changed.emit()

    def _getinstructions(self):
        """ Getter for instructions Property """
        return self._instructions

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
        if self.results:
            suite_result = self.results.overallResult()
        return suite_result

    result_changed = Signal()
    result = Property(str, _getresult, None, notify=result_changed)
