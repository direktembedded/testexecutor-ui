from PySide2.QtCore import QObject, QJsonDocument
from PySide2.QtCore import Signal, Property, Slot
from PySide2.QtWidgets import QApplication
from PySide2.QtCore import QUrl
from PySide2.QtCore import Qt
from PySide2.QtCore import QCoreApplication
from PySide2.QtGui import QIcon
from PySide2.QtQml import QQmlApplicationEngine

import os
import sys
import json

class MultiTestWindowModel(QObject):

    def __init__(self, suiteGroup=None, title="Test Executor", closeHeading="There Are Still Tests Running", closeText="Stop all suites if you want to quit"):
        QObject.__init__(self)
        self._title = title
        self._abortCallback = None
        self._closeHeading = closeHeading
        self._closeText = closeText
        self._allowAbort = False
        self._config = None
        self._suiteGroup = suiteGroup
        if suiteGroup is not None and suiteGroup.abortAll is not None:
            self._abortCallback = suiteGroup.abortAll
            self._allowAbort = True
            self._closeText = "Do you want to abort all tests?"

    def _settitle(self, title):
        """ Setter for title Property """
        if self._title != title:
            self._title = title
            self.title_changed.emit()

    def _gettitle(self):
        """ Getter for title Property """
        return self._title

    title_changed = Signal()
    title = Property(str, _gettitle, _settitle, notify=title_changed)

    def _setcloseHeading(self, closeHeading):
        """ Setter for closeHeading Property """
        if self._closeHeading != closeHeading:
            self._closeHeading = closeHeading
            self.closeHeading_changed.emit()

    def _getcloseHeading(self):
        """ Getter for closeHeading Property """
        return self._closeHeading

    closeHeading_changed = Signal()
    closeHeading = Property(str, _getcloseHeading, _setcloseHeading, notify=closeHeading_changed)

    def _setcloseText(self, closeText):
        """ Setter for closeText Property """
        if self._closeText != closeText:
            self._closeText = closeText
            self.closeText_changed.emit()

    def _getcloseText(self):
        """ Getter for closeText Property """
        return self._closeText

    closeText_changed = Signal()
    closeText = Property(str, _getcloseText, _setcloseText, notify=closeText_changed)

    def _setallowAbort(self, allowAbort):
        """ Setter for allowAbort Property """
        if self._allowAbort != allowAbort:
            self._allowAbort = allowAbort
            self.allowAbort_changed.emit()

    def _getallowAbort(self):
        """ Getter for allowAbort Property """
        return self._allowAbort

    allowAbort_changed = Signal()
    allowAbort = Property(bool, _getallowAbort, _setallowAbort, notify=allowAbort_changed)

    def _setconfig(self, config):
        """ Setter for config Property """
        if self._config != config:
            self._config = config
            self.config_changed.emit()

    def _getconfig(self):
        """ Getter for config Property """
        return self._config

    config_changed = Signal()
    config = Property(str, _getconfig, _setconfig, notify=config_changed)


    @Slot()
    def abortAll(self):
        print("abortAll")
        if self._abortCallback:
            self._abortCallback()

    def exec(self):
        current_path = os.path.dirname(os.path.abspath(__file__))
        relative_path = os.path.join(current_path, "..")
        ui_path = os.path.join(relative_path, 'ui')
        qml_file = os.path.join(ui_path, 'MultiTestWindow.qml')
        url = QUrl.fromLocalFile(qml_file)
        iconFile = os.path.join(ui_path, 'te-64x64.ico')

        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
        QCoreApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
        app = QApplication(sys.argv)

        app.setWindowIcon(QIcon(iconFile))
        check_json = json.loads(self.config)
        engine = QQmlApplicationEngine()
        engine.rootContext().setContextProperty("app_model", self)
        engine.rootContext().setContextProperty("contextKeyValueItemConfig",
                                                json.dumps(check_json["identification"]["item"]))
        engine.rootContext().setContextProperty("model_list", self._suiteGroup)

        engine.load(url)

        return app.exec_()

