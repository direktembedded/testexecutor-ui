/*
 * Copyright 2020 Direkt, Australia
 * Copyright 2021 Direkt Embedded Pty Ltd
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

import QtQuick

/*
 * A qml item which acts as the default configuration for the test suite widget.
 * If the inheriting model wants to override this model they can do so by forcefully setting the config property
 * of the TestSuiteWidget.qml file with equivalent json string. Note the full json needs to be set or some aspects
 * of the UI will fail due to missing configuration.
 */
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
      "identification": 0.25,
      "input": 0.05,
      "instructions": 0.4,
      // results takes remaining space
      "status": 0.04
    }

    /*
     * viewableCount: The number of test results to be visible. Effects height of each test result, dependent on
     *                proportion values set.
     * color: Background color when no items in list
     * item: Set to false here, in order to use default config from ResultItemConfig.
     *       User should define it to an equivalent json to ResultItemConfig it they want to override the default.
     */
    property var results: {
      "viewableCount": 8,
      "color": "#e5e2e2",
      "item": false
    }

    /*
     * color: Background color when no items in list
     * item: Set to false here, in order to use default config from KeyValueItemConfig.
     *       User should define it to an equivalent json to KeyValueItemConfig it they want to override the default.
     */
    property var identification: {
      "color": "#e5e2e2",
      "item": false
    }

    /*
     * allow_focus: allow for the input to automatically get focus when the instruction becomes active
     */
    property var input: {
      "allow_focus": true
    }

    /*
     * color: Background color when instruction text is not html
     * proportion:
     *    header: Proportion of text box dedicated to header if there is one
     *    text: Proportion of text box the main instruction text height will be
     *    control: Proportion of instruction box the control buttons are in height
     */
    property var instructions: {
      "color": {"default": "#f4f2f2", "active": "yellow"},
      "proportion": {"header": 0.1, "textHeight": 0.07, "control": 0.02}
    }
}