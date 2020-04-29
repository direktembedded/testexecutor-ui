"""
Copyright (c) 2020 Direkt, Australia
Licensed under BSD-3-Clause, refer LICENSE file
"""
# This Python file uses the following encoding: utf-8
from PySide2.QtCore import Slot
from PySide2.QtCore import Signal
from PySide2.QtCore import Property
from PySide2.QtCore import QObject
from PySide2.QtCore import QWaitCondition


class ControlButtonConfig(QObject):

    def __init__(self, text=None):
        QObject.__init__(self)
        self._text = text

    def _settext(self, text):
        """ Setter for text Property """
        if self._text != text:
            en = self.enabled
            self._text = text
            self.text_changed.emit()
            if en is not self.enabled:
                self.enable_changed.emit()

    def _gettext(self):
        """ Getter for text Property """
        return self._text

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
        self._buttons = [ControlButtonConfig(), ControlButtonConfig()]
        self._controlReceived = None
        self._waiting = False
        self.userDecisionWait = QWaitCondition()

    def requestDecision(self, buttontextList):
        self._controlReceived = None
        self._waiting = True
        self.setButtons(buttontextList)

    def lastUserDecision(self):
        """
        Obtain the last user decision that was chosen by the user, or None if no decision pending.
        The decision is not cleared until the next call to requestDecision.
        Current implementation returns the lower case of the text on the control buttons. This is not a clean solution
        and should be changed by adding a decision string list to requestDecision instead.
        :return: decision string
        """
        decision = self._controlReceived
        if decision:
            decision = decision.lower()
        return decision

    @Slot(str)
    def onControl(self, decision):
        self._controlReceived = decision
        self.userDecisionWait.wakeAll()

    def cancelWaiting(self):
        self._controlReceived = None
        self.userDecisionWait.wakeAll()

    def setButtons(self, buttonTextList):
        info = buttonTextList
        if type(buttonTextList) is str:
            info = [buttonTextList]
        if type(info) is list:
            i = 0
            for txt in info:
                self._buttons[i].text = txt
                i = i + 1
            for j in range(i, len(self._buttons)):
                self._buttons[j].text = None

    # TODO: Consider modifying to provide more buttons, rather than fixed right left.
    def _getleftButton(self):
        """ Getter for leftButton Property """
        return self._buttons[0]

    leftButton_changed = Signal()
    leftButton = Property(QObject, _getleftButton, None, notify=leftButton_changed)

    def _getrightButton(self):
        """ Getter for rightButton Property """
        return self._buttons[1]

    rightButton_changed = Signal()
    rightButton = Property(QObject, _getrightButton, None, notify=rightButton_changed)


class InstructionModel(QObject):

    def __init__(self):
        QObject.__init__(self)
        self._instructionText = None
        self._control = InstructionControl()
        self._enabled = False
        self._instructionTitle = None
        self._instructionText = None

    @Slot(str, str, list)
    def userDecision(self, title, message, control):
        """
        Method called to send instructions to the user
        :param name: unique name of the test, not used
        :param message: class containing information to display to the user
        :param control: list of text to display on decision/control buttons
        :return: None if no return info, otherwise action information is returned.
                 TODO detail the kind of responses that could be possible
        """
        self.instructionTitle = title
        self.instructionText = message
        self.control.requestDecision(control)

    def _setinstructionText(self, instructionText):
        """ Setter for instructionText Property """
        if self._instructionText != instructionText:
            self._instructionText = instructionText
            if "html" not in instructionText.lower():
                if "\r\n" in instructionText:
                    self._instructionText = instructionText.replace("\r\n", "<br/>")
                if "\n" in self._instructionText:
                    self._instructionText = instructionText.replace("\n", "<br/>")
            self.instructionText_changed.emit()

    def _getinstructionText(self):
        """ Getter for instructionText Property """
        return self._instructionText

    instructionText_changed = Signal()
    instructionText = Property(str, _getinstructionText, _setinstructionText, notify=instructionText_changed)

    def _setinstructionTitle(self, instructionTitle):
        """ Setter for instructionTitle Property """
        if self._instructionTitle != instructionTitle:
            self._instructionTitle = instructionTitle
            self.instructionTitle_changed.emit()

    def _getinstructionTitle(self):
        """ Getter for instructionTitle Property """
        return self._instructionTitle

    instructionTitle_changed = Signal()
    instructionTitle = Property(str, _getinstructionTitle, _setinstructionTitle, notify=instructionTitle_changed)

    def _setcontrol(self, control):
        """ Setter for control Property """
        if self._control != control:
            self._control = control
            self.control_changed.emit()

    def _getcontrol(self):
        """ Getter for control Property """
        return self._control

    control_changed = Signal()
    control = Property(QObject, _getcontrol, _setcontrol, notify=control_changed)

    def _setenabled(self, enabled):
        """ Setter for enabled Property """
        if not enabled:
            # If we have been disabled, ensure there is no pending control blocking operation
            self.control.cancelWaiting()
        if self._enabled != enabled:
            self._enabled = enabled
            self.enabled_changed.emit()

    def _getenabled(self):
        """ Getter for enabled Property """
        return self._enabled

    enabled_changed = Signal()
    enabled = Property(bool, _getenabled, _setenabled, notify=enabled_changed)
