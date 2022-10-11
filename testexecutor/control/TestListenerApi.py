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
Interface class as an interface between test runners/executors and user interfaces and other listeners.
"""


class TestListenerApi(object):
    def test_started(self, name):
        pass

    def test_completed(self, name, result):
        pass

    def test_progress(self, name, progress):
        pass

    def feedback(self, name, data):
        pass

    def user_input(self, title, message, control=None, default_value=None, hidden=False, *values):
        pass

    def user_decision(self, title, message, control):
        pass

    def user_instructions(self, title, message, expect_response=True, control=None):
        pass

    def suite_start(self, name, tests=None):
        pass

    def suite_end(self, name, failures=-1, message=None):
        pass

    def suite_abort(self, name, message):
        pass

    def async_instructions(self, title, message, callback=None, control=None, response=None):
        pass

    def clear_instructions(self):
        pass
