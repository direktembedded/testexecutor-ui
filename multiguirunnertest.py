"""
Test module to kick off text-executor gui.
execute as python3 <filename.py>

Copyright (c) 2020 Direkt, Australia
Licensed under BSD-3-Clause, refer LICENSE.txt
"""
from PySide2.QtWidgets import QApplication
from PySide2.QtQuick import QQuickView
from PySide2.QtCore import QUrl
from PySide2.QtCore import Qt
from PySide2.QtCore import Slot, Signal, QObject
from PySide2.QtGui import QStandardItemModel

import os
import sys

from model.KeyValueModel import KeyValueModel
from model.ResultModel import ResultModel
from model.TestSuiteModel import TestSuiteModel, TestSuiteGroup

app = QApplication([])
view = QQuickView()
current_path = os.path.dirname(sys.argv[0])
ui_path = os.path.join(current_path, 'ui')
qml_file = os.path.join(ui_path, 'MultiTestWidget.qml')
url = QUrl.fromLocalFile(qml_file)


myModel = KeyValueModel()
myModel.populate()

myResults = ResultModel()
myResults.populate()
myResults2 = ResultModel()
myResults2.populate2()

def input_callback(id):
    print("In input callback, got id", id)

mySuiteGroup = TestSuiteGroup()
mySuite = TestSuiteModel(resultlist=myResults, setid_callback=input_callback)
mySuite2 = TestSuiteModel(resultlist=myResults2, setid_callback=input_callback)
mySuiteGroup.addData(mySuite)
mySuiteGroup.addData(mySuite2)
mySuiteGroup.addData(mySuite2)
mySuiteGroup.addData(mySuite2)

FROM, SUBJECT, DATE = range(3)

def addMail(model, mailFrom, subject, date):
    model.insertRow(0)
    model.setData(model.index(0, FROM), mailFrom)
    model.setData(model.index(0, SUBJECT), subject)
    model.setData(model.index(0, DATE), date)

myTreeModel = QStandardItemModel(0, 3, view)
myTreeModel.setHeaderData(FROM, Qt.Horizontal, "From")
myTreeModel.setHeaderData(SUBJECT, Qt.Horizontal, "Subject")
myTreeModel.setHeaderData(DATE, Qt.Horizontal, "Date")

# define a new slot that receives a string and has
# 'saySomeWords' as its name
@Slot()
def screenUpdate():
    print('in screenUpdate')
    myModel2 = KeyValueModel(clone = myModel)
    view.rootContext().setContextProperty("keyValueList", myModel2)
    view.update()

class Connector(QObject):
    updateSignal = Signal()
connector = Connector()

connector.updateSignal.connect(screenUpdate)

import threading
def adddata():
    #myModel.add('ANOTHER','grey')
    myModel.changeme('GREY', '9876543210')
    # doesn't work - view.rootContext().setContextProperty("identifierList", myModel)
    value = {b'name': 'appended', b'result': "blue"}
    connector.updateSignal.emit()

timer = threading.Timer(5.0, adddata)
timer.start()

view.setSource(url)
view.setResizeMode(QQuickView.SizeRootObjectToView)
if view.status() == QQuickView.Error:
    oops = view.errors()
    print(oops)
    import sys
    sys.exit(-1)
else:
    view.rootContext().setContextProperty("treeViewModel", myTreeModel)
    view.rootContext().setContextProperty("model_list", mySuiteGroup)
    view.rootContext().setContextProperty("keyValueList", myModel)
    view.showMaximized()

app.exec_()
timer.cancel()


