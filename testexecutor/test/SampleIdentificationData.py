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

import string
from testexecutor.model.KeyValueModel import KeyValueModel
from testexecutor.model.KeyValueModel import KeyValue


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

    def input_filter(self, values):
        self.setPossibleValues(self.List, ['', 'one', 'two', 'three'])
        for value in values.split('\n'):
            if value.isalpha():
                self.setValue(SampleIdentificationData.Model, value)
            elif value.isdigit():
                self.setValue(SampleIdentificationData.SerialNumber, value)
            elif value.isalnum() and all(c in string.hexdigits for c in value):
                self.setValue(SampleIdentificationData.Mac, value)
            else:
                if value is not None and value != "":
                    self.setValue(SampleIdentificationData.OtherId, value)

    SerialNumber = 'SN'
    Model = 'Model'
    Mac = 'Address'
    OtherId = 'OtherId'
    List = 'List'
