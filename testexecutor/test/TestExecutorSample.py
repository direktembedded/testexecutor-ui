"""
Test module to kick off text-executor gui and run a number of dummy tests in a python thread.
execute as python3 <filename.py>

Copyright (c) 2020 Direkt, Australia
Licensed under BSD-3-Clause, refer LICENSE
"""

from testexecutor.model.TestSuiteGroup import TestSuiteGroup
from testexecutor.model.MultiTestWindowModel import MultiTestWindowModel
from testexecutor.test.SampleTestSuiteWrapper import SampleTestSuiteWrapper

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

    # messy style: material
    # workable styles: fusion, imagine, universal
    #sys.argv += ['--style', 'fusion']

    windowModel = MultiTestWindowModel(mySuiteGroup, "Multiple Runner")
    windowModel.config = config

    exit(windowModel.exec())
