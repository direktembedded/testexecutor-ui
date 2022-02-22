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

Rectangle {
    id: sectionDelegate
    property alias text: txt.text
    property alias indicator: expansion_indicator.text
    property alias count: count.text
    property var selected: false
    property var proportion
    property var config: SectionConfig{}
    signal expandClick()
    signal sectionClick()
    color: getBackgroundColor()
    border.color: config ? config.border.color : "black"
    border.width: config ? config.border.width : 0
    height: config ? config.dimension.height : 25

    RowLayout {
        anchors.fill: parent
        Text {
            id: expansion_indicator
            font.pixelSize: parent.height / 1.3
            font.bold: true
            color: config ? config.text.color.default : null
            Layout.preferredWidth: parent.width * (proportion ? proportion.indicator : 0.02 )
            horizontalAlignment: Text.AlignLeft
            MouseArea {
                anchors.fill: parent
                onClicked: {
                    sectionDelegate.expandClick()
                }
            }
        }
        Text {
            id: txt
            Layout.alignment: Qt.AlignHCenter
            Layout.preferredWidth: parent.width * (proportion ? proportion.indicator : 0.15 )
            font.pixelSize: parent.height / 1.3
            font.bold: true
            Layout.fillHeight: true
            Layout.fillWidth: true
            color: config ? config.text.color.default : null
            leftPadding: 3
            MouseArea {
                anchors.fill: parent
                onClicked: {
                    sectionDelegate.sectionClick()
                }
            }
        }
        Text {
            id: count
            Layout.preferredWidth: parent.width * (proportion ? proportion.count : 0.03 )
            font.pixelSize: parent.height / 1.3
            font.bold: true
            rightPadding: 3
            color: config ? config.text.color.default : null
            horizontalAlignment: Text.AlignRight
        }
    }
    function getBackgroundColor() {
        var color = selected ? "burlywood" : null
        if (config) {
            color = selected ? config.color.selected : config.color.default
        }
        return color
    }
}