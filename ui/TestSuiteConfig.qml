/*
 * A qml item which acts as the default configuration for the test suite widget.
 * If the inheriting model wants to override this model they can do so by forcefully setting the config property
 * of the TestSuiteWidget.qml file with equivalent json string. Note the full json needs to be set or some aspects
 * of the UI will fail due to missing configuration.
 *
 * Copyright (c) 2020 Direkt, Australia
 * Licensed under BSD-3-Clause, refer LICENSE
 */
import QtQuick 2.0

Item {
    property var states: {
      "idle": { "color": "lightgray"},
      "ready": { "color": "gray"},
      "running": { "color": "gray"},
      "stopped": { "color": "orange"},
    }
    property var proportion: {
      "title": 0.1,
      "identification": 0.3,
      "instructions": 0.5,
      // results takes remaining space
      "status": 0.04
    }
}