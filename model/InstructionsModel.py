"""
Copyright (c) 2020 Direkt, Australia
Licensed under BSD-3-Clause, refer LICENSE file
"""
# This Python file uses the following encoding: utf-8
from PySide2.QtCore import Slot
from PySide2.QtCore import Signal
from PySide2.QtCore import Property
from PySide2.QtCore import QObject


class ControlButtonConfig(QObject):

    def __init__(self, text="--"):
        QObject.__init__(self)
        self._text = text

    def _settext(self, text):
        """ Setter for text Property """
        if self._text != text:
            en = self.enabled
            print("en", en)
            self._text = text
            self.text_changed.emit()
            if en is not self.enabled:
                print("enabled changed")
                self.enable_changed.emit()

    def _gettext(self):
        """ Getter for text Property """
        return self._text

    text_changed = Signal()
    text = Property(str, _gettext, _settext, notify=text_changed)

    def _getenabled(self):
        """ Getter for enabled Property """
        en = (self._text is not None) and (self._text is not "")
        print ("test", self._text, "getenabled", en)
        return en

    enable_changed = Signal()
    enabled = Property(str, _getenabled, None, notify=enable_changed)


class InstructionControl(QObject):
    
    def __init__(self):
        QObject.__init__(self)
        self._buttons = [ControlButtonConfig(), ControlButtonConfig()]

    def getEnabled(self):
        return self._buttonLeft.enabled and self._buttonRight.enabled

    def setButtons(self, buttonTextList):
        info = buttonTextList
        if type(buttonTextList) is str:
            info = [buttonTextList]
        if type(info) is list:
            i = len(self._buttons) - 1
            for txt in info:
                self._buttons[i].text = txt
                i = i - 1
            for j in range(i, -1, -1):
                self._buttons[i].text = None

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

    @Slot(str, str, list)
    def userDecision(self, name, message, control):
        """
        Method called to send instructions to the user
        :param name: unique name of the test, not used
        :param message: class containing information to display to the user
        :param control: list of text to display on decision/control buttons
        :return: None if no return info, otherwise action information is returned.
                 TODO detail the kind of responses that could be possible
        """
        self.instructionText = message
        print("userDecision", name, message, control)
        self.control.setButtons(control)

    def _setinstructionText(self, instructionText):
        """ Setter for instructionText Property """
        if self._instructionText != instructionText:
            self._instructionText = instructionText
            self.instructionText_changed.emit()

    def _getinstructionText(self):
        """ Getter for instructionText Property """
        return self._instructionText

    instructionText_changed = Signal()
    instructionText = Property(str, _getinstructionText, _setinstructionText, notify=instructionText_changed)

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
