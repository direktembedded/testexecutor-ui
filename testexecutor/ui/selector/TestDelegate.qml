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
import QtQuick.Layouts


Item {
    property bool expanded: true
    property var dynamic_height: 40
    width: parent ? parent.width : 100
    clip: true
    height: expanded ? dynamic_height : 0
    property var proportion: {"name": 0.15}
    property var config: TestConfig{}

    signal testClick(variant model)

    Rectangle {
        color: getBackgroundColor()
        anchors.fill: parent
        RowLayout {
            anchors.fill: parent
            Text {
                id: nameText
                Layout.preferredWidth: parent.width * (proportion ? proportion.name : 0.15)
                clip: true
                text: model.name
                font.pixelSize: dynamic_height / 1.3
                color: config ? config.text.color.default : "black"
            }
            Text {
                id: descriptionText
                Layout.fillHeight: true
                Layout.fillWidth: true
                clip: true
                text: model.description
                font.pixelSize: dynamic_height / 1.3
                color: config ? config.text.color.default : "black"
                leftPadding: 3
            }
        }

        MouseArea {
            anchors.fill: parent
            onClicked: {
                model.selected = !model.selected
                testClick(model)
            }
        }
        Behavior on height {
            NumberAnimation { duration: 100 }
        }
    }
    function getBackgroundColor() {
        var color = model.selected ? "burlywood" : "white"
        if (config) {
            color = model.selected ? config.color.selected : config.color.default
        }
        return color
    }
}
