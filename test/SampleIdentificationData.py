"""
Copyright (c) 2020 Direkt, Australia
Licensed under BSD-3-Clause, refer LICENSE
"""
import string
from model.KeyValueModel import KeyValueModel
from model.KeyValueModel import KeyValue


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
        self.add(self.SerialNumber, KeyValue('S/N', ''))
        self.add(self.Model, KeyValue(self.Model, ''))
        self.add(self.Mac, KeyValue(self.Mac, ''))
        self.add(self.OtherId, KeyValue(self.OtherId, ''))
        self.add(self.List, KeyValue(self.List, ''), ['', 'one', 'two', 'three'])

    def hasModel(self):
        return self.getValue(self.Model) and self.getValue(self.Model) != ""

    def input_filter(self, value):
        if value.isalpha():
            print("isalpha:", value)
            self.setValue(SampleIdentificationData.Model, value)
        elif value.isdigit():
            print("isdigit:", value)
            self.setValue(SampleIdentificationData.SerialNumber, value)
        elif value.isalnum() and all(c in string.hexdigits for c in value):
            print("ishex:", value)
            self.setValue(SampleIdentificationData.Mac, value)
        else:
            if value is not None and value != "":
                print("other:", value)
                self.setValue(SampleIdentificationData.OtherId, value)

    SerialNumber = 'SN'
    Model = 'Model'
    Mac = 'Address'
    OtherId = 'OtherId'
    List = 'List'
