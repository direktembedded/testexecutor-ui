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
Test module to demonstrate an example test sequence/suite.
This class' run command is called to start executing tests in a separate thread, the tests of which perform callbacks
on the listener to provide user feedback of tests being run.
"""

import threading
import time

from testexecutor.model.ResultModel import Result

ExampleInstance = 1


class SampleTestExecution:
    """
    A class which provides a set of dummy test runs, which are used by SampleTestSuiteWrapper to demonstrate how
    tests can use the testexecutor.TestListenerApi to connect to the testexecuter UI.
    """

    def __init__(self, listener, exit_callback=None, timeout=1.0):
        self._listener = listener
        self._timeout = timeout
        self._runner = None
        self._running = False
        self._exit_callback = exit_callback
        self._prepare_tests()

    def run(self, name=None):
        self._name = name
        if not self._runner:
            self._runner = threading.Thread(target=self._threads_run, args=(name,))
            self._running = True
            self._runner.start()

    def stop(self):
        self._running = False

    def _prepare_tests(self):
        """
        Return one of a multiple of tests groups, so different suites will have different 'virtual' test runs.
        :return: list of test names, and pass or fail state.
        """
        global ExampleInstance
        self._tests = self._testGroups[ExampleInstance % len(self._testGroups)]
        ExampleInstance = ExampleInstance + 1

    def _threads_run(self, name):
        """
        Each test is identical bar the name, and slowly runs through a set of fixed steps as an example.
        :return:
        """
        # TODO: add every second to not include full self._tests list to test that GUI can handle adding tests as they
        # come along, rather than expecting a whole list of tests
        testnames = []
        for test in self._tests:
            testnames.append(test["name"])
        self._listener.suiteStart(name, None)
        fail_count = 0
        for test in self._tests:
            if self._running:
                self._runTest(test)
        if len(self._tests) > 10:
            tname = self._tests[5]["name"]
            self._listener.testStarted(tname)
            self._listener.feedback(tname, "Restarted test only")
        if self._running:
            self._listener.suiteEnd(name, failures=fail_count, message="")
        if self._exit_callback:
            self._exit_callback()

    def _runTest(self, test):
        if test["type"] == 0:
            self._runTest0(test)
        elif test["type"] == 1:
            self._runTest1(test)
        else:
            self._runTest2(test)

    def _runTest0(self, test):
        tname = test["name"]
        self._listener.testStarted(tname)
        time.sleep(self._timeout / 6)
        self._listener.feedback(tname, "Do something")
        time.sleep(self._timeout / 6)
        self._listener.testProgress(tname, 10)
        time.sleep(self._timeout / 6)
        decision = self._listener.userDecision("Select Test Result", "Click\nNo to fail\nYes to continue")
        if decision == "no":
            self._listener.testCompleted(tname, result=Result.StateFail)
            return
        self._listener.testProgress(tname, 30)
        time.sleep(self._timeout / 6)
        self._listener.testProgress(tname, 50)
        self._listener.userInstructions("", ["There is no title but please go ahead and do something for me anyway by pressing Ok", "You can do it"], True, control=["Just do it"])
        time.sleep(self._timeout / 6)
        self._listener.userInstructions("", self._exampleHtml, True)
        time.sleep(self._timeout)
        self._listener.testProgress(tname, 70)
        time.sleep(self._timeout / 6)
        self._listener.testCompleted(tname, result=test["result"])

    def _runTest1(self, test):
        tname = test["name"]
        self._listener.testStarted(tname)
        time.sleep(self._timeout / 6)
        self._listener.feedback(tname, "Doing something")
        j = 1
        for i in range(1,90,5):
            time.sleep(self._timeout / 5)
            self._listener.testProgress(tname, i)
            self._listener.feedback(tname, "{0}".format(i))
            self._listener.userInstructions("Step {0}".format(int(j)), "The test is still working on step {0}".format(int(j)), False)
            j = j + 0.3
        self._listener.feedback(tname, "{0}".format(100))
        self._listener.clearInstructions()
        self._listener.testCompleted(tname, result=test["result"])

    def _runTest2(self, test):
        tname = test["name"]
        self._listener.testStarted(tname)
        self._listener.feedback(tname, "Quick test")
        time.sleep(1)
        self._listener.clearInstructions()
        self._listener.testCompleted(tname, result=test["result"])

    _testGroups = [
        [
            {"name": "test one", "result": Result.StatePass, "type": 1},
            {"name": "test two", "result": False, "type": 1},
            {"name": "test three", "result": True, "type": 1},
            {"name": "test four", "result": Result.StatePass, "type": 1},
            {"name": "test five", "result": True, "type": 1},
            {"name": "test six", "result": False, "type": 1}
        ],
        [
            {"name": "flash", "result": Result.StatePass, "type": 0},
            {"name": "console", "result": Result.StatePass, "type": 0},
            {"name": "ethernet", "result": Result.StatePass, "type": 1},
            {"name": "serial", "result": Result.StatePass, "type": 1},
            {"name": "usb", "result": Result.StatePass, "type": 1},
            {"name": "buttons", "result": Result.StatePass, "type": 1}
        ],
        [
            {"name": "test 1", "result": True, "type": 2},
            {"name": "test 2", "result": False, "type": 2},
            {"name": "test 3", "result": Result.StatePass, "type": 2},
            {"name": "test 4", "result": Result.StatePass, "type": 2},
            {"name": "test 5", "result": Result.StatePass, "type": 2},
            {"name": "test 6", "result": Result.StateFail, "type": 2},
            {"name": "test 7", "result": Result.StatePass, "type": 2},
            {"name": "test 8", "result": Result.StateFail, "type": 2},
            {"name": "test 9", "result": Result.StatePass, "type": 2},
            {"name": "test 10", "result": Result.StatePass, "type": 2},
            {"name": "test 11", "result": Result.StatePass, "type": 2},
            {"name": "test 12", "result": Result.StateFail, "type": 2},
            {"name": "test 13", "result": Result.StatePass, "type": 2},
            {"name": "test 14", "result": Result.StateFail, "type": 2},
            {"name": "test 15", "result": Result.StatePass, "type": 2},
            {"name": "test 16", "result": Result.StatePass, "type": 2},
            {"name": "test 17", "result": Result.StatePass, "type": 2},
            {"name": "test 18", "result": Result.StateFail, "type": 2}
        ],
    ]

    _exampleHtml = """
<html>
    <body style="background-color:orange; height: 100%; font-size:large; font-weight:400; font-style:normal; text-decoration:none; min-height: 100%">
        <h1 align="center" style=" margin-top:2px; margin-bottom:2px; margin-left:0px; margin-right:2px; -qt-block-indent:0; text-indent:0px;">
          <span style=" font-size:large; font-weight:600;">Example Html Instruction</span>
        </h1>
        <p style=" margin-top:12px; margin-bottom:2px; margin-left:4px; margin-right:2px; -qt-block-indent:0; text-indent:0px; font-size:small;">
            <span style=" font-style:italic; font-size:small">
                A subset of html can be used to format instructions for clarity
            </span>
        </p>
        <p style="margin-top:12px; margin-bottom:2px; margin-left:4px; margin-right:4px; -qt-block-indent:0; text-indent:0px; font-size:small;">
            <span style="font-size:small;">For information of what html subset refer to</span>
            <br/> 
            <a style="font-size:small;" href="https://doc.qt.io/qt-5/richtext-html-subset.html">
                https://doc.qt.io/qt-5/richtext-html-subset.html
            </a>              
        </p>
        <p style=" margin-top:12px; margin-bottom:12px; margin-left:4px; margin-right:4px; -qt-block-indent:0; text-indent:0px;">
            <span style=" font-size:large;">Supported are </span>
            <span style=" font-size:small; font-weight:600;">bold</span>
            <span style=" font-size:small;">, </span>
            <span style=" font-size:small; font-style:italic;">italic</span>
            <span style=" font-size:small;">, and </span>
            <span style=" font-size:small; text-decoration: underline;">underlined</span>
            <span style=" font-size:small;"> font styles, and </span>
            <span style=" font-size:small; font-weight:600; color:#00007f;">multicolored</span>
            <span style=" font-size:small;"> </span>
            <span style=" font-size:small; font-weight:600; color:#aa0000;">text</span>
            <br/>
            <span style=" font-size:small;">Font families such as </span>
            <span style=" font-family:'Times New Roman'; font-size:small; font-weight:600;">Times New Roman</span>
            <span style=" font-size:small;"> and </span>
            <span style=" font-family:'Courier'; font-size:small; font-weight:600;">Courier</span>
            <span style=" font-size:small;"> can also be used directly. </span>
        </p>
        <p align="center" style="margin-top:12px; margin-bottom:2px; margin-left:4px; margin-right:4px; -qt-block-indent:0; text-indent:0px; font-size:small;">
            <span style=" font-style:italic;">
                To extend html background color at the end of the instruction, you can use line breaks.
            </span>
        </p>
        <br/>
        <br/>
        <br/>
        <br/>
        <br/>
        <br/>
    </body>
</html>
"""
