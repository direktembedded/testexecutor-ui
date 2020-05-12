"""
Test module to kick off text-executor gui.
execute as python3 <filename.py>

Copyright (c) 2020 Direkt, Australia
Licensed under BSD-3-Clause, refer LICENSE
"""
from PySide2.QtWidgets import QApplication
from PySide2.QtQuick import QQuickView
from PySide2.QtCore import QUrl
from PySide2.QtCore import Qt
from PySide2.QtCore import QCoreApplication
from PySide2.QtQml import QQmlApplicationEngine
from PySide2.QtGui import QIcon

import os
import sys

from model.TestSuiteGroup import TestSuiteGroup
from test.SampleTestSuiteWrapper import SampleTestSuiteWrapper

if __name__ == "__main__":
    current_path = os.path.dirname(sys.argv[0])
    ui_path = os.path.join(current_path, 'ui')
    qml_file = os.path.join(ui_path, 'MultiTestWindow.qml')
    url = QUrl.fromLocalFile(qml_file)
    iconFile = os.path.join(ui_path, 'te-64x64.ico')

    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(iconFile))
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QCoreApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    mySuiteGroup = TestSuiteGroup()
    for i in range(6):
        mySuiteGroup.addData(SampleTestSuiteWrapper("Station {0}".format(i)))

    engine = QQmlApplicationEngine(url)
    engine.rootContext().setContextProperty("model_list", mySuiteGroup)

    exit(app.exec_())
