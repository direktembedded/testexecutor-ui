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
from PySide6.QtCore import Slot
from PySide6.QtCore import Signal
from PySide6.QtCore import Property
from PySide6.QtCore import QObject
from PySide6.QtGui import Qt


class ControlButtonConfig(QObject):

    def __init__(self, text=None):
        QObject.__init__(self)
        self.lock = threading.RLock()
        self._text = text

    def _settext(self, text):
        """ Setter for text Property """
        en = self.enabled
        changed = False
        with self.lock:
            if self._text != text:
                self._text = text
                changed = True
        if changed:
            self.text_changed.emit()
            if en is not self.enabled:
                self.enable_changed.emit()

    def _gettext(self):
        """ Getter for text Property """
        with self.lock:
            t = self._text
        return t

    text_changed = Signal()
    text = Property(str, _gettext, _settext, notify=text_changed)

    def _getenabled(self):
        """ Getter for enabled Property """
        en = (self._text is not None) and (self._text != "")
        return en

    enable_changed = Signal()
    enabled = Property(bool, _getenabled, None, notify=enable_changed)


class InstructionControl(QObject):
    
    def __init__(self):
        QObject.__init__(self)
        self.lock = threading.RLock()
        self._buttons = [ControlButtonConfig(), ControlButtonConfig()]
        self._controlReceived = None
        self._inputReceived = None
        self._expectInput = False
        self.userInputEvent = threading.Event()

    onUserInput = Signal(str, str)

    def requestDecision(self, buttontextList):
        with self.lock:
            self._controlReceived = None
            self._inputReceived = None
        return self.setButtons(buttontextList)

    def lastUserDecision(self):
        """
        Obtain the last user decision that was chosen by the user, or None if no decision pending.
        The decision is not cleared until the next call to requestDecision.
        Current implementation returns the lower case of the text on the control buttons. This is not a clean solution
        and should be changed by adding a decision string list to requestDecision instead.
        :return: decision string
        """
        with self.lock:
            decision = self._controlReceived
            if decision:
                decision = decision.lower()
        return decision

    def lastUserInput(self):
        """
        Obtain the last user input decision that was chosen by the user, or None if no decision pending.
        The decision is not cleared until the next call to requestDecision.
        :return: decision string
        """
        with self.lock:
            input = self._inputReceived
        return input

    def clear(self):
        self.cancelWaiting()
        self.setButtons([])

    @Slot(str)
    def onControl(self, decision):
        """
        A callback called once a button has been pressed in the instruction window.
        onControl does not clear the instruction window, as the caller may wish to have multiple callbacks.
        This means the caller needs to clear the instruction window when it wants to.
        :param decision: The button press or decision made
        :return:
        """
        self._onControl(decision)

    def _onControl(self, decision, input_value=None):
        with self.lock:
            self._controlReceived = decision
            self._inputReceived = input_value
        self.userInputEvent.set()
        self.onUserInput.emit(self.lastUserDecision(), self.lastUserInput())

    @Slot(str)
    def onExternalInput(self, input_value):
        """
        A callback providing input from a relevant external control. The control should be supplied externally to
        this component and provide complete string input.
        """
        if input_value:
            self._onControl(self.USER_INPUT, input_value)

    def cancelWaiting(self):
        self._controlReceived = None
        self.userInputEvent.set()

    def setButtons(self, buttonTextList):
        info = buttonTextList
        if type(buttonTextList) is str:
            info = [buttonTextList]
        with self.lock:
            if type(info) is list:
                i = 0
                for txt in info:
                    self._buttons[i].text = txt
                    i = i + 1
                for j in range(i, len(self._buttons)):
                    self._buttons[j].text = None
        present = False
        if buttonTextList:
            present = len(info) > 0
        return present

    def lastWasUserInput(self):
        return self.lastUserDecision() == self.USER_INPUT

    # TODO: Consider modifying to provide more buttons, rather than fixed right left.
    def _getleftButton(self):
        """ Getter for leftButton Property """
        with self.lock:
            b = self._buttons[0]
        return b

    leftButton_changed = Signal()
    leftButton = Property(QObject, _getleftButton, None, notify=leftButton_changed)

    def _getrightButton(self):
        """ Getter for rightButton Property """
        with self.lock:
            b = self._buttons[1]
        return b

    rightButton_changed = Signal()
    rightButton = Property(QObject, _getrightButton, None, notify=rightButton_changed)

    USER_INPUT = 'te_input'

class InstructionModel(QObject):

    def __init__(self):
        QObject.__init__(self)
        self.lock = threading.RLock()
        self._instructionText = None
        self._control = InstructionControl()
        self._enabled = False
        self._input_hidden = False
        self._instructionTitle = None
        self._instructionText = None

    def clear(self):
        self.instructionTitle = ""
        self.instructionText = ""
        self.control.clear()

    @Slot(str, str, list, bool)
    def userDecision(self, title, message, control, enable=True):
        """
        Method called to send instructions to the user
        The caller will use control.lastUserDecision() to obtain the decision chosen, implementing a wait state
        if required.
        If no control information is given, then this model will remain disabled as their is no expectation for the
        user to provide input.
        :param name: unique name of the test, not used
        :param message: class containing information to display to the user
        :param control: list of text to display on decision/control buttons
        :param enable: enable text widget even if no buttons so highlighted colour is shown
        :return: None
        """
        self.instructionTitle = title
        self.instructionText = message
        buttons_enabled = self.control.requestDecision(control)
        self._internal_setenabled(buttons_enabled | enable)

    @Slot(str, str, list, str, bool, tuple, bool)
    def userInputRequest(self, title, message, control, default_value=None, hidden=False, values=None, enable=True):
        """
        Method called to send instructions to the user
        The caller will use control.lastUserDecision() to obtain the decision chosen, implementing a wait state
        if required.
        If no control information is given, then this model will remain disabled as their is no expectation for the
        user to provide input.
        :param name: unique name of the test, not used
        :param message: class containing information to display to the user
        :param control: list of text to display on decision/control buttons
        :param default_value: value to provide as a default to the user - future
        :param values: enable text widget even if no buttons so highlighted colour is shown - future
        :param enable: enable text widget even if no buttons so highlighted colour is shown
        :param hidden: hide text as entered
        :return: None
        """
        self.instructionTitle = title
        self.instructionText = message
        self.input_hidden = hidden
        buttons_enabled = self.control.requestDecision(control)
        self._internal_setenabled(buttons_enabled | enable)

    def userDecisionWait(self):
        """
        If the caller wishes to block until the user decision requested is made, they can call this immediately
        after calling userDecision.
        """
        self.control.userInputEvent.clear()
        self.control.userInputEvent.wait()

    def _setinstructionText(self, instructionText):
        """ Setter for instructionText Property """
        changed = False
        with self.lock:
            if self._instructionText != instructionText:
                changed = True
                self._instructionText = instructionText
                if instructionText and "html" not in instructionText.lower():
                    self._instructionText = Qt.convertFromPlainText(instructionText, Qt.WhiteSpaceNormal)

        if changed:
            self.instructionText_changed.emit()

    def _getinstructionText(self):
        """ Getter for instructionText Property """
        with self.lock:
            instr = self._instructionText
        return instr

    instructionText_changed = Signal()
    instructionText = Property(str, _getinstructionText, _setinstructionText, notify=instructionText_changed)

    def _setinstructionTitle(self, instructionTitle):
        """ Setter for instructionTitle Property """
        changed = False
        with self.lock:
            if self._instructionTitle != instructionTitle:
                self._instructionTitle = instructionTitle
                changed = True
        if changed:
            self.instructionTitle_changed.emit()

    def _getinstructionTitle(self):
        """ Getter for instructionTitle Property """
        with self.lock:
            t = self._instructionTitle
        return t

    instructionTitle_changed = Signal()
    instructionTitle = Property(str, _getinstructionTitle, _setinstructionTitle, notify=instructionTitle_changed)

    def _setcontrol(self, control):
        """ Setter for control Property """
        changed = False
        with self.lock:
            if self._control != control:
                self._control = control
                changed = True
        if changed:
            self.control_changed.emit()

    def _getcontrol(self):
        """ Getter for control Property """
        with self.lock:
            c = self._control
        return c

    control_changed = Signal()
    control = Property(QObject, _getcontrol, _setcontrol, notify=control_changed)

    def _internal_setenabled(self, enabled):
        changed = False
        with self.lock:
            if self._enabled != enabled:
                self._enabled = enabled
                changed = True
        if changed:
            self.enabled_changed.emit()

    def _setenabled(self, enabled):
        """ Setter for enabled Property """
        if not enabled:
            # If we have been disabled, ensure there is no pending control blocking operation
            self.control.cancelWaiting()
        self._internal_setenabled(enabled)

    def _getenabled(self):
        """ Getter for enabled Property """
        with self.lock:
            e = self._enabled
        return e

    enabled_changed = Signal()
    enabled = Property(bool, _getenabled, _setenabled, notify=enabled_changed)

    def _set_input_hidden(self, input_hidden):
        """ Setter for _input_hidden Property """
        changed = False
        with self.lock:
            if self._input_hidden != input_hidden:
                self._input_hidden = input_hidden
                changed = True
        if changed:
            self.input_hidden_changed.emit()

    def _get_input_hidden(self):
        """ Getter for _input_hidden Property """
        with self.lock:
            e = self._input_hidden
        return e

    input_hidden_changed = Signal()
    input_hidden = Property(bool, _get_input_hidden, _set_input_hidden, notify=input_hidden_changed)
