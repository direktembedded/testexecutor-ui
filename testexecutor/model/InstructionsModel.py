"""
Copyright (c) 2020 Direkt, Australia
Licensed under BSD-3-Clause, refer LICENSE file
"""
# This Python file uses the following encoding: utf-8
import threading
from PySide2.QtCore import Slot
from PySide2.QtCore import Signal
from PySide2.QtCore import Property
from PySide2.QtCore import QObject


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
        en = (self._text is not None) and (self._text is not "")
        return en

    enable_changed = Signal()
    enabled = Property(bool, _getenabled, None, notify=enable_changed)


class InstructionControl(QObject):
    
    def __init__(self):
        QObject.__init__(self)
        self.lock = threading.RLock()
        self._buttons = [ControlButtonConfig(), ControlButtonConfig()]
        self._controlReceived = None
        self.userDecisionEvent = threading.Event()

    onUserDecision = Signal(str)

    def requestDecision(self, buttontextList):
        with self.lock:
            self._controlReceived = None
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

    def clear(self):
        self.cancelWaiting()
        self.setButtons([])

    @Slot(str)
    def onControl(self, decision):
        with self.lock:
            self._controlReceived = decision
        self.setButtons([])  # Do not allow for a second button press by clearing all buttons
        self.userDecisionEvent.set()
        self.onUserDecision.emit(self.lastUserDecision())

    def cancelWaiting(self):
        self._controlReceived = None
        self.userDecisionEvent.set()

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


class InstructionModel(QObject):

    def __init__(self):
        QObject.__init__(self)
        self.lock = threading.RLock()
        self._instructionText = None
        self._control = InstructionControl()
        self._enabled = False
        self._instructionTitle = None
        self._instructionText = None

    def clear(self):
        self.instructionTitle = ""
        self.instructionText = ""
        self.control.clear()

    @Slot(str, str, list)
    def userDecision(self, title, message, control):
        """
        Method called to send instructions to the user
        The caller will use control.lastUserDecision() to obtain the decision chosen, implementing a wait state
        if required.
        If no control information is given, then this model will remain disabled as their is no expectation for the
        user to provide input.
        :param name: unique name of the test, not used
        :param message: class containing information to display to the user
        :param control: list of text to display on decision/control buttons
        :return: None
        """
        self.instructionTitle = title
        self.instructionText = message
        self.enabled = self.control.requestDecision(control)

    def userDecisionWait(self):
        """
        If the caller wishes to block until the user decision requested is made, they can call this immediately
        after calling userDecision.
        """
        self.control.userDecisionEvent.clear()
        self.control.userDecisionEvent.wait()

    def _setinstructionText(self, instructionText):
        """ Setter for instructionText Property """
        changed = False
        with self.lock:
            if self._instructionText != instructionText:
                changed = True
                self._instructionText = instructionText
                if "html" not in instructionText.lower():
                    if "\r\n" in instructionText:
                        self._instructionText = instructionText.replace("\r\n", "<br/>")
                    if "\n" in self._instructionText:
                        self._instructionText = instructionText.replace("\n", "<br/>")
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

    def _setenabled(self, enabled):
        """ Setter for enabled Property """
        if not enabled:
            # If we have been disabled, ensure there is no pending control blocking operation
            self.control.cancelWaiting()
        changed = False
        with self.lock:
            if self._enabled != enabled:
                self._enabled = enabled
                changed = True
        if changed:
            self.enabled_changed.emit()

    def _getenabled(self):
        """ Getter for enabled Property """
        with self.lock:
            e = self._enabled
        return e

    enabled_changed = Signal()
    enabled = Property(bool, _getenabled, _setenabled, notify=enabled_changed)
