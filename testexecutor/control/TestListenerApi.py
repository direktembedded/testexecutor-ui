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

"""
Interface class as an interface between test runners/executors and user interfaces.
"""


class TestListenerApi(object):
    def testStarted(self, name):
        pass

    def testCompleted(self, name, result):
        pass

    def testProgress(self, name, progress):
        pass

    def feedback(self, name, data):
        pass

    def userInput(self, title, message):
        return None

    def userDecision(self, title, message, control):
        return None

    def userInstructions(self, title, message, expectResponse = True, control=None):
        return None

    def suiteStart(self, name="test run", tests=None):
        pass

    def suiteEnd(self, name="test run", failures=-1, message=""):
        pass

    def suiteAbort(self, name="test run", message=""):
        pass

    def asyncInstructions(self, title, message, callback=None, control=None, response=None):
        pass

    def clearInstructions(self):
        pass
