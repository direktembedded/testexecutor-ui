from PySide2.QtCore import Signal
from PySide2.QtCore import Qt
from PySide2.QtCore import QObject
from PySide2.QtCore import QMutex

from model.TestSuiteModel import TestSuiteModel
from control.TestListenerApi import TestListenerApi


class Link(QObject):
    addSignal = Signal(str, str)
    startSignal = Signal(str)
    populateSignal = Signal(list)
    feedbackSignal = Signal(str, str)
    endSignal = Signal(str, str)
    progressSignal = Signal(str, int)
    userDecisionSignal = Signal(str, str, list)
    userWaitMutex = QMutex()


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
        self.link.userDecisionSignal.connect(self.model.instructions.userDecision, Qt.BlockingQueuedConnection)

    # Test Listener Api methods
    def testStarted(self, name):
        self.link.startSignal.emit(name)

    def testCompleted(self, name, result):
        self.link.endSignal.emit(name, result)

    def testProgress(self, name, progress):
        self.link.progressSignal.emit(name, progress)

    def feedback(self, name, data):
        self.link.feedbackSignal.emit(name, data)

    def userInput(self, title, message):
        """
        Place holder for allowing user to return a value
        Unused currently
        """
        pass

    def userDecision(self, title, message):
        buttons = ["Yes", "No"]
        self.link.userWaitMutex.lock()
        self.link.userDecisionSignal.emit(title, message, buttons)
        self.model.instructions.control.userDecisionWait.wait(self.link.userWaitMutex)
        self.link.userWaitMutex.unlock()
        return self.model.instructions.control.lastUserDecision()

    def userInstructions(self, title, message, expectResponse=True):
        buttons = []
        if expectResponse:
            buttons = ["Ok"]
        self.link.userWaitMutex.lock()
        self.link.userDecisionSignal.emit(title, message, buttons)
        if expectResponse:
            self.model.instructions.control.userDecisionWait.wait(self.link.userWaitMutex)
            self.clearInstructions()
        self.link.userWaitMutex.unlock()
        return self.model.instructions.control.lastUserDecision()

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

    def clearInstructions(self):
        self.link.userDecisionSignal.emit(None, None, None)
