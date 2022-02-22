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
import QtQuick.Layouts
import QtQuick.Controls

Item {
    id: keyValueItem
    width:parent.width
    height: 40
    clip: true
    property var config: KeyValueItemConfig {}

    Binding {
        target: model.value
        property: "value"
        value: valueIsArray() ? comboControl.currentText : identifier.text
    }

    Rectangle {
        id: rectangle
        width: parent.width
        color: config.color
        border.width: 1
        border.color: config.border.color
        anchors.fill: parent

        RowLayout {
            id: row
            height: parent.height
            spacing: 1.5
            anchors.fill: parent

            Rectangle {
                id: keyLabelRectangle
                Layout.preferredWidth: parent.width * config.proportion.name
                color: config.name.color
                Layout.alignment: Qt.AlignLeft | Qt.AlignTop
                border.color: config.name.border.color
                border.width: 1
                Layout.fillHeight: true

                Text {
                    id: identifierName
                    color: config.name.text.color
                    text: value.label
                    verticalAlignment: Text.AlignVCenter
                    anchors.rightMargin: 2
                    anchors.fill: parent
                    font.pixelSize: parent.height * 0.7
                    minimumPixelSize: 10
                    elide: Text.ElideLeft
                    horizontalAlignment: Text.AlignRight
                    ToolTip {
                        visible: identifierName.truncated ? mouseArea.containsMouse : false
                        timeout: 3000
                        delay: 500
                        contentItem:
                            Column {
                                Text {
                                    text: identifierName.text
                                    font.pixelSize: identifier.height
                                    font.weight: Font.ExtraBold
                                }
                            }
                    }
                    MouseArea {
                        id: mouseArea
                        anchors.fill: parent
                        hoverEnabled: true
                    }
                }
            }

            Rectangle {
                id: valueRectangle
                Layout.fillHeight: true
                color: config.value.color
                Layout.fillWidth: true
                border.width: 1
                border.color: config.value.border.color
                ComboBox {
                    id: comboControl
                    implicitHeight: parent.height
                    height: parent.height * 1.2
                    width: parent.width
                    font.pixelSize: parent.height * 0.85
                    model: possibles
                    visible: valueIsArray()
                    bottomPadding: height * 0.3
                    leftPadding: 2
                    rightPadding: 0
                    contentItem: Text {
                        leftPadding: 0
                        rightPadding: comboControl.indicator ? comboControl.indicator.width + comboControl.spacing : 0
                        text: comboControl.displayText
                        font: comboControl.font
                        verticalAlignment: Text.AlignVCenter
                        elide: Text.ElideRight
                    }
                    ToolTip {
                        visible: comboControl.currentText ? comboControl.hovered : false
                        timeout: 3000
                        delay: 500
                        contentItem:
                            Column {
                                Text {
                                    text: comboControl.currentText
                                    font.pixelSize: identifier.height
                                    font.weight: Font.ExtraBold
                                }
                            }
                    }

                    delegate: ItemDelegate {
                        width: comboControl.width
                        contentItem: Text {
                            text: modelData
                            font: comboControl.font
                            elide: Text.ElideRight
                            verticalAlignment: Text.AlignVCenter
                            padding: 0
                        }
                        highlighted: comboControl.highlightedIndex === index
                    }
                    background: Rectangle {
                        border.width: 1
                        border.color: config.value.border.color
                    }
                }

                TextInput {
                    id: identifier
                    text: value.value
                    color: config.value.text.color
                    visible: !valueIsArray()
                    activeFocusOnPress: false
                    autoScroll: true
                    clip: true
                    font.pixelSize: parent.height / 1.2
                    anchors.rightMargin: 0
                    anchors.leftMargin: 3
                    anchors.fill: parent
                    ToolTip {
                        visible: parent.text ? identifierMouseArea.containsMouse : false
                        timeout: 3000
                        delay: 500
                        contentItem:
                            Column {
                                Text {
                                    text: identifier.text
                                    font.pixelSize: identifier.height
                                    font.weight: Font.ExtraBold
                                }
                            }
                    }
                    MouseArea {
                        id: identifierMouseArea
                        anchors.fill: parent
                        hoverEnabled: true
                    }
                }
            }
        }
    }

    Component.onCompleted: parseConfigStr()

    function valueIsArray() {
        return (possibles.length > 1) ? true : false;
    }
    function parseConfigStr() {
        if (typeof contextKeyValueItemConfig !== "undefined") {
            var json = JSON.parse(contextKeyValueItemConfig)
            keyValueItem.config = json
        }
    }
}

