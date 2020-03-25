"""
Copyright (c) 2020 Direkt, Australia
Licensed under BSD-3-Clause, refer LICENSE.txt
"""
from model.TestSuiteModel import TestSuiteModel
from model.ResultModel import ResultModel
from test.SampleIdentificationData import SampleIdentificationData
from test.SampleTestExecution import SampleTestExecution

class SampleTestSuiteWrapper(TestSuiteModel):
    """
    A class that wraps the base TestSuiteModel and provides some test specific functionality, like the callback
    function for the identification widget, and the state control button callback.
    """
    def __init__(self):
        self._id_data = SampleIdentificationData()
        self._id_data.populate()
        self._results = ResultModel()
        self._results.populate()
        self._testrun = None
        TestSuiteModel.__init__(self, self._id_data, self._results, self._input_filter,
                                setstate_callback=self._state_control_callback)
        self.suitestate = TestSuiteModel.STATE_IDLE

    def _start_suite(self):
        if not self._testrun:
            self._testrun = SampleTestExecution()
            self._testrun.run()

    def _stop_suite(self):
        self._testrun.stop()

    def _state_control_callback(self, st):
        newstate = None
        if st == TestSuiteModel.STATE_NEXT:
            if self.suitestate == TestSuiteModel.STATE_READY or not self.suitestate:
                newstate = TestSuiteModel.STATE_RUNNING
            elif self.suitestate == TestSuiteModel.STATE_RUNNING:
                newstate = TestSuiteModel.STATE_STOPPED
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
