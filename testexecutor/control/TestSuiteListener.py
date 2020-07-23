"""
Copyright (c) 2020 Direkt, Australia
Licensed under BSD-3-Clause, refer LICENSE file
"""

from PySide2.QtCore import Signal
from PySide2.QtCore import Slot
from PySide2.QtCore import Qt
from PySide2.QtCore import QObject
from PySide2.QtCore import QMutex

from testexecutor.model.TestSuiteModel import TestSuiteModel
from testexecutor.control.TestListenerApi import TestListenerApi


class Link(QObject):
    """
    A class which is the linke between this modules 'Python" TestSuiteListener and the Qt/Qml UI.
    It simply provides some Qt Signals and Slots which correspond to the PySide2 models Slots and Signals.
    """
    addSignal = Signal(str, str)
    startSignal = Signal(str)
    populateSignal = Signal(list)
    feedbackSignal = Signal(str, str)
    endSignal = Signal(str, str)
    progressSignal = Signal(str, int)
    userDecisionSignal = Signal(str, str, list)
    _userCallback = None

    def setAsyncInstructionCallback(self, signal, callback):
        self._userCallback = callback
        signal.connect(self._asyncInstructionCallback, Qt.QueuedConnection)

    @Slot(str)
    def _asyncInstructionCallback(self, response):
        if self._userCallback:
            self._userCallback(response)
            self._userCallback = None


class TestSuiteListener(TestListenerApi):

    PASS = "Pass"
    FAIL = "Fail"

    def __init__(self, model=None):
        """
        Connect the Qml UI with our listener through a Link object which holds our connection Qt signals and slots.
        :param model: A testexecutor.model.TestSuiteModel which this listener will connect to.
        """
        self.model = model
        self.link = Link()
        self.link.addSignal.connect(self.model.results.add, Qt.QueuedConnection)
        self.link.startSignal.connect(self.model.results.start, Qt.QueuedConnection)
        self.link.populateSignal.connect(self.model.results.populateTests, Qt.QueuedConnection)
        self.link.feedbackSignal.connect(self.model.results.setFeedback, Qt.QueuedConnection)
        self.link.endSignal.connect(self.model.results.end, Qt.QueuedConnection)
        self.link.progressSignal.connect(self.model.results.progress, Qt.QueuedConnection)
        self.link.userDecisionSignal.connect(self.model.instructions.userDecision, Qt.QueuedConnection)

    # Test Listener Api methods
    def testStarted(self, name):
        """
        Should be called by the underlying test whenever it is started, allowing the listener (likely UI) to add it
        or indicate it is running.
        :param name: Name of the test that has been started
        :return: None
        """
        self.link.startSignal.emit(name)

    def testCompleted(self, name, result):
        resultStr = result
        if type(result) is bool:
            resultStr = self.FAIL
            if result:
                resultStr = self.PASS
        self.link.endSignal.emit(name, resultStr)

    def testProgress(self, name, progress):
        """
        Update the progress of the test with name.
        :param name: Name of the test to update the progress on
        :param progress: Percentage of progress, 0 to 100
        :return: None
        """
        self.link.progressSignal.emit(name, progress)

    def feedback(self, name, data):
        """
        Update the feedback information (likely shown to user on UI) for the test with name.
        :param name: Name of test to show feedback for
        :param data: string containing feedback
        :return: None
        """
        self.link.feedbackSignal.emit(name, data)

    def userInput(self, title, message):
        """
        Place holder for allowing user to return a value
        Unused currently
        """
        pass

    def userDecision(self, title, message, control=["Yes", "No"]):
        """
        Request a yes or no user decision. This is a blocking call and will not return until user has made a decision
        or test is cancelled/stopped.
        :param title: Top line of the question posed to the user
        :param message: message asked of the user
        :param control: Alternate button/control values. First two only used.
        :return: The decision made as "yes" or "no" string by default, or control values
        """
        buttons = control
        self.link.userDecisionSignal.emit(title, message, buttons)
        self.model.instructions.userDecisionWait()
        self.clearInstructions()
        return self.model.instructions.control.lastUserDecision()

    def userInstructions(self, title, message, expectResponse=True):
        """
        Provides user instructions. By default acknowledgement is requested (paramter expectResponse is true) and the
        user should press "Ok" to continue
        :param title: Top line of the question posed to the user
        :param message: message asked of the user
        :param expectResponse: set to false if not response is required from user.
                               i.e. if this is only a test step detail.
        :return: "ok" if response requested, else None or ""
        """
        buttons = []
        if expectResponse:
            buttons = ["Ok"]
        self.link.userDecisionSignal.emit(title, message, buttons)
        if expectResponse:
            self.model.instructions.userDecisionWait()
            self.clearInstructions()
        return self.model.instructions.control.lastUserDecision()

    def suiteStart(self, name="test run", tests=[]):
        """
        This should be called by test execution module/thread whenever a new suite is started to ensure the listener
        (likely a UI) can update its state to indicate the suite is in progress.
        TODO name is not used, could add a title to the model.
        :param name: The name of the test suite run. Currently not used.
        :param tests: The tests to run
        :return: nothing
        """
        self.link.populateSignal.emit(tests)
        self.model.suitestate = TestSuiteModel.STATE_RUNNING

    def suiteEnd(self, name="test run", failures=-1, message=""):
        """
        This should be called by the test execution module/thread whenever a suite has been completed to
        ensure the listener (likely a UI) can update its state to indicate the suite has been completed.
        If the suite is cancelled/aborted use suiteAbort.
        :param name: The name of the test suite run. Currently not used.
        :param failures: The number of test failures
        :param message: A message to display to the user. Currently not used.
        :return: None
        """
        self.model.suitestate = TestSuiteModel.STATE_END

    def suiteAbort(self, name="test run", message=""):
        """
        This should be called by the test execution module/thread whenever a suite has been cancelled or aborted to
        ensure the listener (likely a UI) can update its state to indicate this.
        :param name: The name of the test suite run. Currently not used.
        :param message: A message to display to the user. Currently not used.
        :return: None
        """
        self.model.suitestate = TestSuiteModel.STATE_STOPPED

    def asyncInstructions(self, title, message, callback=None, control=[], response=[]):
        """
        A non blocking instruction provided to the user. The callback will be called when the instruction control
        action is taken.
        Usage would be
          listener.asyncInstructions("Do something", "Press the start button", callback=self.myAction, control=["Start", "Stop"])
        and the callback would be
          def myAction(self, response=None):
              if response and response == "start":
                  self.start()
              else:
                  self.stop()
        :param title: The first line of the instructions provided to user
        :param message: The message request made of the user
        :param callback: The function to call of type callback("response") where "response" is the control text if a
                         string is not specified in the response array.
        :param control: An array of strings to display in the control buttons.
        :param response: a set of response strings to use. Should correspond to the control entries. Currently not used.
        :return: None
        """
        self.link.setAsyncInstructionCallback(self.model.instructions.control.onUserDecision, callback)
        self.link.userDecisionSignal.emit(title, message, control)

    def clearInstructions(self):
        """
        Infor the listener to clear the instruction window.
        :return: None
        """
        self.link.userDecisionSignal.emit(None, None, None)
