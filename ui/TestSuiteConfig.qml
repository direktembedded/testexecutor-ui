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
    /*
     * Configuration variables set dependent on the state of the suite.
     * idle.color is set in idle and end states if suite does not have a 'pass' or 'fail' state. If it does then the
     *            pass or fail colours will be used.
     * ready.color is set when suite is ready to start
     * running.color is set when suite state is starting or running
     * stopped.color is set when the suite is stopping or stopped state
     */
    property var states: {
      "idle": { "color": {"default": "lightgray", "pass": "green", "fail": "red"}, "button": {"text": "Clear"} },
      "ready": { "color": "gray", "button": {"text": "Clear"}},
      "running": { "color": "gray", "button": {"text": "Stop"}},
      "stopped": { "color": "orange", "button": {"text": "Clear"}},
    }
    /*
     * Define the proportions for the height of the test suite widget.
     * The results area is not defined and will fill any remaining area.
     */
    property var proportion: {
      "title": 0.1,
      "identification": 0.3,
      "instructions": 0.4,
      // results takes remaining space
      "status": 0.04
    }
    /*
     * viewableCount: The number of test results to be visible. Effects height of each test result, dependent on
     *                proportion values set.
     */
    property var results: {
      "viewableCount": 10
    }
}