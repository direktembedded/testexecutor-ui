from PySide2.QtCore import Signal
from PySide2.QtCore import Qt
from PySide2.QtCore import QObject

from model.TestSuiteModel import TestSuiteModel
from control.TestListenerApi import TestListenerApi


class Link(QObject):
    addSignal = Signal(str, str)
    startSignal = Signal(str)
    populateSignal = Signal(list)
    feedbackSignal = Signal(str, str)
    endSignal = Signal(str, str)
    progressSignal = Signal(str, int)


class TestSuiteListener(TestListenerApi):
    def __init__(self, model=None):
        self.model = model
        self.link = Link()
        self.link.addSignal.connect(self.model.results.add, Qt.QueuedConnection)
        self.link.startSignal.connect(self.model.results.start, Qt.QueuedConnection)
        self.link.populateSignal.connect(self.model.results.populateTests, Qt.QueuedConnection)
        self.link.feedbackSignal.connect(self.model.results.setFeedback, Qt.QueuedConnection)
        self.link.endSignal.connect(self.model.results.end, Qt.QueuedConnection)
        self.link.progressSignal.connect(self.model.results.progress, Qt.QueuedConnection)

    # Test Listener Api methods
    def testStarted(self, name):
        self.link.startSignal.emit(name)

    def testCompleted(self, name, result):
        self.link.endSignal.emit(name, result)

    def testProgress(self, name, progress):
        self.link.progressSignal.emit(name, progress)

    def feedback(self, name, data):
        self.link.feedbackSignal.emit(name, data)

    def userInput(self, name, message):
        return None

    def userDecision(self, name, message):
        return None

    def userInstructions(self, name, message, expectResponse=True):
        return None

    def suiteStart(self, name="test run", tests=[]):
        """
        TODO name is not used, could add a title to the model.
        :param name: The name of the test suite run
        :param tests: The tests to run
        :return: nothing
        """
        self.link.populateSignal.emit(tests)
        self.model.suitestate = TestSuiteModel.STATE_RUNNING

    def suiteEnd(self, name="test run", failures=-1, message=""):
        self.model.suitestate = TestSuiteModel.STATE_IDLE
        pass

    def suiteAbort(self, name="test run", message=""):
        self.model.suitestate = TestSuiteModel.STATE_STOPPED
        pass
