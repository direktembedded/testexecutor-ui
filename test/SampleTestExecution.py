"""
Test module to demonstrate an example test sequence/suite.
This class' run command is called to start executing tests in a separate thread, the tests of which perform callbacks
on the listener to provide user feedback of tests being run.

Copyright (c) 2020 Direkt, Australia
Licensed under BSD-3-Clause, refer LICENSE.txt
"""
import threading
import time

from model.ResultModel import Result

ExampleInstance = 1

class SampleTestExecution:

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
        print("Suite exiting")

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
        print("Started new runner thread")
        testnames = []
        for test in self._tests:
            testnames.append(test["name"])
        self._listener.suiteStart(name, None)
        fail_count = 0
        for test in self._tests:
            if self._running:
                tname = test["name"]
                self._listener.testStarted(tname)
                self._listener.feedback(tname, "Doing something")
                self._listener.testProgress(tname, 0.5)
                self._listener.testCompleted(tname, result=test["result"])
                time.sleep(self._timeout)
        if self._running:
            self._listener.suiteEnd(name, failures=fail_count, message="")
        if self._exit_callback:
            self._exit_callback()

    _testGroups = [
        [
            {"name": "test one", "result": Result.StatePass},
            {"name": "test two", "result": Result.StateFail},
            {"name": "test three", "result": Result.StatePass},
            {"name": "test four", "result": Result.StatePass},
            {"name": "test five", "result": Result.StatePass},
            {"name": "test six", "result": Result.StateFail}
        ],
        [
            {"name": "flash", "result": Result.StatePass},
            {"name": "console", "result": Result.StatePass},
            {"name": "ethernet", "result": Result.StatePass},
            {"name": "serial", "result": Result.StatePass},
            {"name": "usb", "result": Result.StatePass},
            {"name": "buttons", "result": Result.StatePass}
        ],
    ]
"""
These are the Listener APIs.
    - def testStarted(self, name):
    - def testCompleted(self, name, result):
    - def testProgress(self, name, progress):
    - def feedback(self, name, data):
    def userInput(self, name, message):
    def userDecision(self, name, message):
    def userInstructions(self, name, message, expectResponse = True):
    - def suiteStart(self, name = "test run", tests=[]):
    - def suiteEnd(self, name="test run", failures=-1, message=""):
    def suiteAbort(self, name="test run", message=""):
"""