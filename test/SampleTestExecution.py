"""
Test module to demonstrate an example test sequence/suite.
This class' run command is called to start executing tests in a separate thread, the tests of which perform callbacks
on the listener to provide user feedback of tests being run.

Copyright (c) 2020 Direkt, Australia
Licensed under BSD-3-Clause, refer LICENSE.txt
"""
import threading
import time


class SampleTestExecution:
    def __init__(self, listener, exit_callback=None, timeout=1.0):
        self._listener = listener
        self._timeout = timeout
        self._runner = None
        self._running = False
        self._exit_callback = exit_callback
        self._prepare_tests()
        self._name = None

    def run(self, name):
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
        :return: list of test names, and pass or fail state
        """
        self._tests = [{"name": "test one", "result": True}, {"name": "test two", "result": False},
                       {"name": "test three", "result": True}, {"name": "test four", "result": True},
                       {"name": "test five", "result": True}, {"name": "test six", "result": False}]

    def _threads_run(self):
        """
        Each test is identical bar the name, and slowly runs through a set of fixed steps as an example.
        :return:
        """
        # TODO: add every second to not include full self._tests list to test that GUI can handle adding tests as they
        # come along, rather than expecting a whole list of tests
        self._listener.suiteStart(self._name, self._tests)
        fail_count = 0
        for test in self._tests:
            if self._running:
                tname = test["name"]
                self._listener.testStarted(tname)
                self._listener.feedback("Doing something")
                self._listener.testProgress(tname, 0.5)
                self._listener.testCompleted(tname, result=test["pass"])
                time.sleep(self._timeout)
        self._listener.suiteEnd(self._name, failures=fail_count, message="")
        if self._exit_callback:
            self._exit_callback()
