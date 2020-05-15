from PySide2.QtCore import QObject
from PySide2.QtCore import Signal, Property, Slot


class MultiTestWindowModel(QObject):

    def __init__(self, abortCallback=None, title="Test Executor", closeHeading=None, closeText=None):
        QObject.__init__(self)
        self._title = title
        self._abortCallback = abortCallback
        self._closeHeading = "There Are Still Tests Running"
        self._closeText = "Stop all suites if you want to quit"
        self._allowAbort = False
        if abortCallback is not None:
            print("allowing abort")
            self._allowAbort = True
            self._closeText = "Do you want to abort all tests?"

    def _settitle(self, title):
        """ Setter for title Property """
        if self._title != title:
            self._title = title
            self.title_changed.emit()

    def _gettitle(self):
        """ Getter for title Property """
        return self._title

    title_changed = Signal()
    title = Property(str, _gettitle, _settitle, notify=title_changed)

    def _setcloseHeading(self, closeHeading):
        """ Setter for closeHeading Property """
        if self._closeHeading != closeHeading:
            self._closeHeading = closeHeading
            self.closeHeading_changed.emit()

    def _getcloseHeading(self):
        """ Getter for closeHeading Property """
        return self._closeHeading

    closeHeading_changed = Signal()
    closeHeading = Property(str, _getcloseHeading, _setcloseHeading, notify=closeHeading_changed)

    def _setcloseText(self, closeText):
        """ Setter for closeText Property """
        if self._closeText != closeText:
            self._closeText = closeText
            self.closeText_changed.emit()

    def _getcloseText(self):
        """ Getter for closeText Property """
        return self._closeText

    closeText_changed = Signal()
    closeText = Property(str, _getcloseText, _setcloseText, notify=closeText_changed)

    def _setallowAbort(self, allowAbort):
        """ Setter for allowAbort Property """
        if self._allowAbort != allowAbort:
            self._allowAbort = allowAbort
            self.allowAbort_changed.emit()

    def _getallowAbort(self):
        """ Getter for allowAbort Property """
        return self._allowAbort

    allowAbort_changed = Signal()
    allowAbort = Property(bool, _getallowAbort, _setallowAbort, notify=allowAbort_changed)

    @Slot()
    def abortAll(self):
        print("abortAll")
        if self._abortCallback:
            self._abortCallback()
