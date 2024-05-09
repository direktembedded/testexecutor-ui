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

from PySide6.QtCore import Signal
from PySide6.QtCore import Slot
from PySide6.QtCore import Qt
from PySide6.QtCore import QObject
from PySide6.QtCore import QMutex

from testexecutor.model.TestSuiteModel import TestSuiteModel
from testexecutor.control.TestListenerApi import TestListenerApi


class Link(QObject):
    """
    A class which is the link between this modules 'Python" TestSuiteListener and the Qt/Qml UI.
    It simply provides some Qt Signals and Slots which correspond to the PySide6 models Slots and Signals.
    """
    addSignal = Signal(str, str)
    startSignal = Signal(str)
    populateSignal = Signal(list, bool)
    feedbackSignal = Signal(str, str)
    endSignal = Signal(str, str)
    progressSignal = Signal(str, int)
    userDecisionSignal = Signal(str, str, list, bool)
    userInputRequestSignal = Signal(str, str, list, str, bool, tuple, bool)
    _userCallback = None

    def __init__(self, instruction_signal):
        QObject.__init__(self)
        instruction_signal.connect(self._asyncInstructionCallback, Qt.QueuedConnection)

    def setAsyncInstructionCallback(self, callback):
        self._userCallback = callback

    @Slot(str)
    def _asyncInstructionCallback(self, response, input):
        if self._userCallback:
            if self._userCallback(response):
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
        self.clear_results_on_start = True
        self.link = Link(self.model.instructions.control.onUserInput)
        self.link.addSignal.connect(self.model.results.add, Qt.QueuedConnection)
        self.link.startSignal.connect(self.model.results.start, Qt.QueuedConnection)
        self.link.populateSignal.connect(self.model.results.populateTests, Qt.QueuedConnection)
        self.link.feedbackSignal.connect(self.model.results.setFeedback, Qt.QueuedConnection)
        self.link.endSignal.connect(self.model.results.end, Qt.QueuedConnection)
        self.link.progressSignal.connect(self.model.results.progress, Qt.QueuedConnection)
        self.link.userDecisionSignal.connect(self.model.instructions.userDecision, Qt.QueuedConnection)
        self.link.userInputRequestSignal.connect(self.model.instructions.userInputRequest, Qt.QueuedConnection)

    # Test Listener Api methods
    def test_started(self, name):
        """
        Should be called by the underlying test whenever it is started, allowing the listener (likely UI) to add it
        or indicate it is running.
        :param name: Name of the test that has been started
        :return: None
        """
        self.clear_instructions()
        self.link.startSignal.emit(name)

    def test_completed(self, name, result):
        resultStr = result
        if type(result) is bool:
            resultStr = self.FAIL
            if result:
                resultStr = self.PASS
        self.link.endSignal.emit(name, resultStr)

    def test_progress(self, name, progress):
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
        self.link.feedbackSignal.emit(name, self._convert_message(data))

    def user_input(self, title, message, control=None, default_value=None, hidden=False, *values):
        """
        Place holder for allowing user to return a value
        :return: (input, decision) e.g. (None, "cancel") or ("Hello", "ok")
        """
        if control is None:
            control = ["Cancel"]
        buttons = control
        # if exception occurs here we get no error and test seems unrecoverable
        self.link.userInputRequestSignal.emit(title, self._convert_message(message), buttons,
                                              default_value, hidden, values, False)
        self.model.instructions.userDecisionWait()
        self.clear_instructions()
        input_value = self.model.instructions.control.lastUserInput()
        decision = self.model.instructions.control.lastUserDecision()
        return input_value, decision

    def user_decision(self, title, message, control=None):
        """
        Request a yes or no user decision. This is a blocking call and will not return until user has made a decision
        or test is cancelled/stopped.
        :param title: Top line of the question posed to the user
        :param message: message asked of the user
        :param control: Alternate button/control values. First two only used.
        :return: The decision made as "yes" or "no" string by default, or control values
        """
        if control is None:
            control = ["Yes", "No"]
        buttons = control
        self.link.userDecisionSignal.emit(title, self._convert_message(message), buttons, False)
        self.model.instructions.userDecisionWait()
        self.clear_instructions()
        decision = self.model.instructions.control.lastUserDecision()
        if self.model.instructions.control.lastWasUserInput():
            # If last entry was user input then interpret it as a button press
            decision = self.model.instructions.control.lastUserInput()
        return decision

    def user_instructions(self, title, message, expectResponse=True, control=None, highlight=True):
        """
        Provides user instructions. By default acknowledgement is requested (paramter expectResponse is true) and the
        user should press "Ok" to continue
        :param title: Top line of the question posed to the user
        :param message: message asked of the user
        :param expectResponse: set to false if not response is required from user.
                               i.e. if this is only a test step detail.
        :param control: list of control buttons strings to show, e.g. ["Yes", "No"]
        :param highlight: enable instruction widget (to show colour) even if no control buttons provided
        :return: "ok" if response requested, else None or ""
        """
        if control is None:
            control = []
        buttons = []
        if expectResponse:
            buttons = ["Ok"]
            if control and type(control) is list and len(control) > 0:
                buttons = control
        self.link.userDecisionSignal.emit(title, self._convert_message(message), buttons, highlight)
        if expectResponse:
            self.model.instructions.userDecisionWait()
            self.clear_instructions()
        return self.model.instructions.control.lastUserDecision()

    def suite_start(self, name="test run", tests=None):
        """
        This should be called by test execution module/thread whenever a new suite is started to ensure the listener
        (likely a UI) can update its state to indicate the suite is in progress.
        :param name: The name of the test suite run. Currently not used.
        :param tests: The tests to run
        :return: nothing
        """
        if tests is None:
            tests = []
        self.link.populateSignal.emit(tests, self.clear_results_on_start)
        self.model.suitestate = TestSuiteModel.STATE_RUNNING

    def suite_end(self, name="test run", failures=-1, message=""):
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

    def suite_abort(self, name="test run", message=""):
        """
        This should be called by the test execution module/thread whenever a suite has been cancelled or aborted to
        ensure the listener (likely a UI) can update its state to indicate this.
        :param name: The name of the test suite run. Currently not used.
        :param message: A message to display to the user. Currently not used.
        :return: None
        """
        self.model.suitestate = TestSuiteModel.STATE_STOPPED

    def async_instructions(self, title, message, callback=None, control=None, response=None):
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
        if control is None:
            control = []
        if response is None:
            response = []
        self.link.setAsyncInstructionCallback(callback)
        self.link.userDecisionSignal.emit(title, self._convert_message(message), control, True)

    def clear_instructions(self):
        """
        Infor the listener to clear the instruction window.
        :return: None
        """
        self.link.userDecisionSignal.emit(None, None, None, False)

    def _convert_message(self, message):
        if type(message) is list:
            message = "\n".join(message)
        return message