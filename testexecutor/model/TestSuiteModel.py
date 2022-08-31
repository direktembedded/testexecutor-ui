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
import time
from PySide6.QtCore import QObject, Qt
from PySide6.QtCore import Signal, Property, Slot
from testexecutor.model.InstructionsModel import InstructionModel


class SuiteColours(QObject):
    """
    Dynamic colours that the user can set on the suite
    If the colour is None/Undefined then the default colour as in
    the configuration will be used.
    """
    def __init__(self):
        QObject.__init__(self)
        self.lock = threading.RLock()
        self._running_colour = None
        self._interaction_colour = None

    def clear(self):
        self.running = None
        self.interaction = None

    def _set_running_colour(self, _running_colour):
        """ Setter for running_colour Property """
        with self.lock:
            self._running_colour = _running_colour
        self.running_colour_changed.emit()

    def _get_running_colour(self):
        """ Getter for running_colour Property """
        with self.lock:
            col = self._running_colour
        return col

    running_colour_changed = Signal()
    running = Property(str, _get_running_colour, _set_running_colour, notify=running_colour_changed)

    def _set_interaction_colour(self, _interaction_colour):
        """ Setter for interaction_colour Property """
        with self.lock:
            self._interaction_colour = _interaction_colour
        self.interaction_colour_changed.emit()

    def _get_interaction_colour(self):
        """ Getter for interaction_colour Property """
        with self.lock:
            col = self._interaction_colour
        return col

    interaction_colour_changed = Signal()
    interaction = Property(str, _get_interaction_colour, _set_interaction_colour,
                                   notify=interaction_colour_changed)


class TestSuiteModel(QObject):
    # these state strings must match those in TestSuiteWidget.qml
    STATE_RUNNING = "running"
    STATE_STARTING = "starting"
    STATE_STOPPING = "stopping"
    STATE_STOPPED = "stopped"
    STATE_END = "end"
    STATE_IDLE = "idle"
    STATE_READY = "ready"
    STATE_RESTART = "restart"
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
        self._controller = None
        self._suite_colours = SuiteColours()
        self.on_input.connect(self.instructions.control.onExternalInput, Qt.QueuedConnection)

    def clear(self):
        self.identifiers.clearData()
        self.instructions.clear()
        self.results.clear()
        time.sleep(0.1)
        self.identifiers.clearData()  # Intentionally duplicate until qml corrected to clear combobox selected item
        self.suitestate = self.STATE_IDLE
        self.suite_colours.clear()

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
        # call id call back only when not active as we do not want to change ids after started
        if not self.active():
            if self.setid_callback:
                self.setid_callback(id)
        else:
            self.on_input.emit(id)
        self.id_changed.emit()

    def _getid(self):
        """ Getter for newid Property """
        id = None
        with self.lock:
            id = self._newId
        return id

    id_changed = Signal()
    on_input = Signal(str)
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

    def _getsuite_colours(self):
        """ Getter for suite_colours Property """
        with self.lock:
            col = self._suite_colours
        return col

    suite_colours_changed = Signal()
    suite_colours = Property(QObject, _getsuite_colours, None, notify=suite_colours_changed)

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

    def _setcontroller(self, controller):
        """ Setter for controller Property """
        changed = False
        with self.lock:
            if self._controller != controller:
                self._controller = controller
                changed = True
        if changed:
            self.controller_changed.emit()

    def _getcontroller(self):
        """
        Getter for controller Property
        A suite can have an attached controller which can be used to define a test list and the like.
        """
        controller = None
        with self.lock:
            controller = self._controller
        return controller

    controller_changed = Signal()
    controller = Property(QObject, _getcontroller, _setcontroller, notify=controller_changed)

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

    def close(self):
        """
        API for Hard closing the suite, ensuring any processes or threads created are killed
        :return:
        """
        pass
