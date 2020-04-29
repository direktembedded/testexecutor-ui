"""
Test module to kick off text-executor gui.
execute as python3 <filename.py>

Copyright (c) 2020 Direkt, Australia
Licensed under BSD-3-Clause, refer LICENSE
"""
from PySide2.QtWidgets import QApplication
from PySide2.QtQuick import QQuickView
from PySide2.QtCore import QUrl

import os
import sys

from model.TestSuiteGroup import TestSuiteGroup
from test.SampleTestSuiteWrapper import SampleTestSuiteWrapper

app = QApplication([])
view = QQuickView()
current_path = os.path.dirname(sys.argv[0])
ui_path = os.path.join(current_path, 'ui')
qml_file = os.path.join(ui_path, 'MultiTestWidget.qml')
url = QUrl.fromLocalFile(qml_file)

mySuiteGroup = TestSuiteGroup()
for i in range(4):
    mySuiteGroup.addData(SampleTestSuiteWrapper("Station {0}".format(i)))

view.setSource(url)
view.setResizeMode(QQuickView.SizeRootObjectToView)
if view.status() == QQuickView.Error:
    oops = view.errors()
    print(oops)
    import sys
    sys.exit(-1)
else:
    view.rootContext().setContextProperty("model_list", mySuiteGroup)
    view.showMaximized()

app.exec_()



