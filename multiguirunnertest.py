"""
Test module to kick off text-executor gui.
execute as python3 <filename.py>

Copyright (c) 2020 Direkt, Australia
Licensed under BSD-3-Clause, refer LICENSE
"""
from PySide2.QtWidgets import QApplication
from PySide2.QtCore import QUrl
from PySide2.QtCore import Qt
from PySide2.QtCore import QCoreApplication
from PySide2.QtQml import QQmlApplicationEngine
from PySide2.QtGui import QIcon

import os
import sys
import json

from model.TestSuiteGroup import TestSuiteGroup
from model.MultiTestWindowModel import MultiTestWindowModel
from test.SampleTestSuiteWrapper import SampleTestSuiteWrapper

config = '''{
    "states": {
      "idle": { "color": {"default": "lightgray", "pass": "green", "fail": "red"}, "button": {"text": "Clear"} },
      "ready": { "color": "gray", "button": {"text": "Clear"}},
      "running": { "color": "gray", "button": {"text": "Stop"}},
      "stopped": { "color": "orange", "button": {"text": "Clear"}}
    },

    "proportion": {
      "title": 0.1,
      "identification": 0.2,
      "instructions": 0.4,
      "status": 0.04
    },

    "results": {
      "viewableCount": 8,
      "color": "#e5e2e2",
      "item": {
        "proportion": {
            "name": 0.3,
            "time": 0.2
        },
        "color": "#605b5b",
        "border": {"color": "#00000000"},
        "name": {
            "color": "#00000000",
            "text": {"color": "#e5e2e2"}
        },
        "feedback": {
            "color": "#8e8a8a",
            "border": {"color": "#b9e5e2e2"},
            "text": {"color": {"default": "black", "progress": "#e5e2e2"}},
            "progress": {"color": "green"}
        },
        "time": {
            "color": "#00000000",
            "text": {"color": "#e5e2e2"}
        }
      }
    },

    "identification": {
      "proportion": {"input": 0.15},
      "item": { 
            "proportion": {
              "name": 0.4
            },
            "color": "#605b5b",
            "border": { "color": "#00000000" },
            "name": {
              "color": "#00000000",
              "text": {"color": "#e5e2e2"},
              "border": {"color": "#00000000"}
            },
            "value": {
              "color": "#ffffff",
              "border": {"color": "#b9e5e2e2"},
              "text": {"color": "black"}
            }
      }
    }
}
'''

if __name__ == "__main__":
    mySuiteGroup = TestSuiteGroup()
    for i in range(6):
        mySuiteGroup.addData(SampleTestSuiteWrapper("Station {0}".format(i)))

    current_path = os.path.dirname(sys.argv[0])
    ui_path = os.path.join(current_path, 'ui')
    qml_file = os.path.join(ui_path, 'MultiTestWindow.qml')
    url = QUrl.fromLocalFile(qml_file)
    iconFile = os.path.join(ui_path, 'te-64x64.ico')

    # messy style: material
    # workable styles: fusion, imagine, universal
    #sys.argv += ['--style', 'fusion']

    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QCoreApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    app = QApplication(sys.argv)

    app.setWindowIcon(QIcon(iconFile))

    windowModel = MultiTestWindowModel(mySuiteGroup.abortAll, "Multiple Runner")
    testJson = json.loads(config)
    windowModel.config = config

    engine = QQmlApplicationEngine()
    engine.rootContext().setContextProperty("app_model", windowModel)
    engine.rootContext().setContextProperty("contextKeyValueItemConfig", json.dumps(testJson["identification"]["item"]))
    engine.rootContext().setContextProperty("model_list", mySuiteGroup)

    engine.load(url)

    exit(app.exec_())
