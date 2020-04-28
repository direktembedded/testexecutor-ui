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

    def userDecision(self, title, message):
        return None

    def userInstructions(self, title, message, expectResponse = True):
        return None

    def suiteStart(self, name = "test run", tests=[]):
        pass

    def suiteEnd(self, name="test run", failures=-1, message=""):
        pass

    def suiteAbort(self, name="test run", message=""):
        pass

