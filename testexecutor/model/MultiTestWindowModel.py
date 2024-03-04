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

from PySide6.QtCore import QObject, QJsonDocument
from PySide6.QtCore import Signal, Property, Slot
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QUrl
from PySide6.QtCore import Qt
from PySide6.QtCore import QCoreApplication
from PySide6.QtGui import QIcon
from PySide6.QtQml import QQmlApplicationEngine

import os
import sys
import json

notice = """
<b>This software includes code from Test Executor ™</b><br/>
<i>Copyright © Direkt Embedded Pty Ltd<br/>
https://www.direktembedded.com</i>"""

class MultiTestWindowModel(QObject):

    def __init__(self, suiteGroup=None, title="Test Executor", closeHeading="There Are Still Tests Running", closeText="Stop all suites if you want to quit"):
        QObject.__init__(self)
        self._title = title
        self._visibility = "Maximized"
        self._abortCallback = None
        self._closeHeading = closeHeading
        self._closeText = closeText
        self._allowAbort = False
        self._config = None
        self._suiteGroup = suiteGroup
        self._about = None
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

    def _setvisibility(self, visibility):
        """ Setter for visibility Property """
        if self._visibility != visibility:
            self._visibility = visibility
            self.visibility_changed.emit()

    def _getvisibility(self):
        """ Getter for visibility Property """
        return self._visibility

    visibility_changed = Signal()
    visibility = Property(str, _getvisibility, _setvisibility, notify=visibility_changed)

    def _setabout(self, about):
        """ Setter for about Property. Expects html (or rich text subset there of) """
        if self._about != about:
            self._about = about
            self.about_changed.emit()

    def _getabout(self):
        """ Getter for about Property """
        return self._add_notice(self._about)

    def _add_notice(self, about):
        if about:
            about = f"{about}<br/>{notice}"
        else:
            about = notice
        return about

    about_changed = Signal()
    about = Property(str, _getabout, _setabout, notify=about_changed)

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


    @Slot(bool)
    def abortAll(self, hard=False):
        if self._abortCallback:
            self._abortCallback(hard)

    def exec(self, iconFile=None):
        current_path = os.path.dirname(os.path.abspath(__file__))
        relative_path = os.path.join(current_path, "..")
        ui_path = os.path.join(relative_path, 'ui')
        qml_file = os.path.join(ui_path, 'MultiTestWindow.qml')
        url = QUrl.fromLocalFile(qml_file)
        if not iconFile:
            iconFile = os.path.join(ui_path, 'te-64x64.ico')

        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
        QCoreApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
        app = QApplication(sys.argv)

        app.setWindowIcon(QIcon(iconFile))
        if self.config:
            check_json = json.loads(self.config)
        engine = QQmlApplicationEngine()
        engine.rootContext().setContextProperty("app_model", self)
        if self.config:
            engine.rootContext().setContextProperty("contextKeyValueItemConfig",
                                                    json.dumps(check_json["identification"]["item"]))
            if "controller" in check_json:
                engine.rootContext().setContextProperty("contextFilterSelectorItemConfig",
                                                    json.dumps(check_json["controller"]["filter"]["item"]))
        engine.rootContext().setContextProperty("model_list", self._suiteGroup)

        engine.load(url)

        return app.exec_()
