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

Item {
    /*
     * Define the proportions for the widths of the test result items.
     * The feedback area is not defined and will fill any remaining area.
     */
    property var proportion: {
        "name": 0.3,
        // feedback fill remaining space
        "time": 0.2
    }
    property var color: "#605b5b"
    property var border: {"color": "#00000000"}
    property var name: {
        "color": "#00000000",
        "text": {"color": "#e5e2e2"}
    }
    property var feedback: {
        "color": "#8e8a8a",
        "border": {"color": "#b9e5e2e2"},
        "text": {"color": {"default": "black", "progress": "#e5e2e2"}},
        "progress": {"color": "green"}
    }
    property var time: {
        "color": "#00000000",
        "text": {"color": "#e5e2e2"}
    }
}