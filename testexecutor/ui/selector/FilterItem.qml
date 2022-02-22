/*
 * Copyright 2020 Sipke Vriend, Australia
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
import QtQuick.Controls

Item {
    id: filterItem
    width: content.paintedWidth + control.width + 10
    height: 30
    property var config: FilterItemConfig{}
    signal remove(int index)

    Rectangle {
        id: filterItemRectangle
        color: Boolean(config) ? filterItem.config.background.color: "white"
        border.width: 1
        border.color: Boolean(config) ? config.border.color : "darkgray"
        anchors.fill: parent
        RowLayout {
            anchors.rightMargin: 3
            anchors.leftMargin: 3
            anchors.bottomMargin: 3
            anchors.topMargin: 3
            anchors.fill: parent
            Text {
                id: content
                text: modelData
                font.pixelSize: parent.height * 0.7
                Layout.fillWidth: true
                Layout.fillHeight: true
            }
            Button {
                id: control
                text: "-"
                Layout.fillHeight: true
                Layout.preferredHeight: parent.height * 0.8
                font.wordSpacing: 0
                font.pixelSize: parent.height > 0 ? parent.height * 0.7 : 10
                font.weight: Font.ExtraBold
                Layout.maximumWidth: 30
                Layout.preferredWidth: 20
                Layout.minimumWidth: 10
                background: Rectangle {
                    border.width: control.activeFocus ? 2 : 1
                    border.color: "darkgray"
                    radius: 4
                    gradient: Gradient {
                        GradientStop { position: 0 ; color: control.pressed ? config.button.gradient.start.pressed : config.button.gradient.start.off }
                        GradientStop { position: 1 ; color: control.pressed ? config.button.gradient.end.pressed : config.button.gradient.end.off }
                    }
                }
                onClicked: {
                    filterItem.remove(index)
                }
            }
        }
    }
}

