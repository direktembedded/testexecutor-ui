"""
Copyright (c) 2020 Direkt, Australia
Licensed under BSD-3-Clause, refer LICENSE.txt
"""
from model.KeyValueModel import KeyValueModel


class SampleIdentificationData(KeyValueModel):
    """
    An example identification class which has four entries in the Test Suite identification widget.
    The four entries split the types of Input data into either alphabet only, number only, alphanumeric or other.
    The input box callback should be supplied to the test suite so that anything entered into the input box will
    be verified by the callback and then one of the given identification boxes updated accordingly.
    """
    def __init__(self, parent=None, clone=None):
        KeyValueModel.__init__(self, parent, clone)

    def populate(self):
        self.add(SampleIdentificationData.Alpha, 'type')
        self.add(SampleIdentificationData.Number, '1')
        self.add(SampleIdentificationData.AlphaNum, 'or2')
        self.add(SampleIdentificationData.Other, 'in Input box')

    def input_filter(self, value):
        if value.isalpha():
            print("isalpha:", value)
            self.setValue(SampleIdentificationData.Alpha, value)
        elif value.isdigit():
            print("isdigit:", value)
            self.setValue(SampleIdentificationData.Number, value)
        elif value.isalnum():
            print("isalnum:", value)
            self.setValue(SampleIdentificationData.AlphaNum, value)
        else:
            print("other:", value)
            self.setValue(SampleIdentificationData.Other, value)

    Alpha = 'Alpha'
    Number = 'Number'
    AlphaNum = 'Alphanum'
    Other = 'Other'
