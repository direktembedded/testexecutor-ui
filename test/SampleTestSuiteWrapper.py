"""
Copyright (c) 2020 Direkt, Australia
Licensed under BSD-3-Clause, refer LICENSE.txt
"""
from model.TestSuiteModel import TestSuiteModel
from model.ResultModel import ResultModel
from test.SampleIdentificationData import SampleIdentificationData


class SampleTestSuiteWrapper(TestSuiteModel):
    """
    A class that wraps the base TestSuiteModel and provides some test specific functionality, like the callback
    function for the identification widget.
    """
    def __init__(self):
        self._id_data = SampleIdentificationData()
        self._id_data.populate()
        self._results = ResultModel()
        self._results.populate()
        TestSuiteModel.__init__(self, self._id_data, self._results, self._id_data.input_filter)
