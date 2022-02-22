/*
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
     * Define the proportions for the widths of the test suite items.
     * The description area is not defined and will fill any remaining area.
     */
    property var proportion: {
        "indicator": 0.02,
        "name": 0.15,
        // descprition takes on remainder
        "count": 0.03
    }
    property var header: HeaderConfig{}
    property var section: SectionConfig{}
    property var row: TestConfig{}
    property var indicators: {0:"⮞", 1:"⮟"}
    property int viewableCount: 25
    property var filter: {
        "item": false
    }
}
