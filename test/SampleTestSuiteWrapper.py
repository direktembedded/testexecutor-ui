"""
Copyright (c) 2020 Direkt, Australia
Licensed under BSD-3-Clause, refer LICENSE
"""
from model.TestSuiteModel import TestSuiteModel
from model.ResultModel import ResultModel
from control.TestSuiteListener import TestSuiteListener
from test.SampleIdentificationData import SampleIdentificationData
from test.SampleTestExecution import SampleTestExecution


class SampleTestSuiteWrapper(TestSuiteModel, TestSuiteListener):
    """
    Class to demonstrate interfacing between TestSuiteWidget GUI and TestSuiteModel and Test Runs which exercise
    the TestListenerApi methods.
    TestSuiteModel functionality, like the callback function for the identification widget, are linked via the
    TestSuiteModel constructor, and suite control business logic written in them.
    The TestListenerApi methods are implement and exercise the TestSuitModel properties directly.
    """
    def __init__(self):
        self._id_data = SampleIdentificationData()
        self._id_data.populate()
        self._results = ResultModel()
        self._testrun = None
        TestSuiteModel.__init__(self, self._id_data, self._results, self._input_filter,
                                setstate_callback=self._state_control_callback)
        self.suitestate = TestSuiteModel.STATE_IDLE
        TestSuiteListener.__init__(self, model=self)

    def _start_suite(self):
        """
        This internal _start_suite will start the new thread which will be the test run execution. The test run in turn
        should call the TestListenerApi's suiteStart
        :return:
        """
        if not self._testrun:
            self._testrun = SampleTestExecution(listener=self, exit_callback=self._on_exit)
            self._testrun.run()

    def _stop_suite(self):
        self._testrun.stop()

    def _state_control_callback(self, st):
        newstate = None
        if st == TestSuiteModel.STATE_NEXT:
            if self.suitestate == TestSuiteModel.STATE_READY or not self.suitestate:
                self.suitestate = TestSuiteModel.STATE_STARTING  # recursive loop risk!
                self._start_suite()
            elif self.suitestate == TestSuiteModel.STATE_RUNNING:
                newstate = TestSuiteModel.STATE_STOPPED
                self._stop_suite()
            else:
                newstate = TestSuiteModel.STATE_IDLE
        else:
            newstate = st
        return newstate

    def _input_filter(self, input):
        """
        For demonstration on the very first input entry, we make the suite state 'ready'
        :param input: The new input text from UI
        :return: None
        """
        self._id_data.input_filter(input)
        if input is not None and input != "":
            self.suitestate = TestSuiteModel.STATE_READY

    def _on_exit(self):
        print("Test Run Exited")
        self._testrun = None
