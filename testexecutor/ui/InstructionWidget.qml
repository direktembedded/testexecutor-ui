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
import QtQuick.Controls
import QtQuick.Layouts

Item {
    id: instructionWidget
    width: parent.width
    height: parent.height
    property var color: "yellow"
    property var proportion: {"header": 0.1, "textHeight": 0.05, "control": 0.1}
    property var model
    property var control_enabled: controlEnabled()

    Binding {
        target: model
        property: "enabled"
        value: instructionWidget.enabled
    }

    Rectangle {
        id: rectangleBase
        width: parent.width
        height: parent.height
        color: "#f4f2f2"
        Layout.fillHeight: true
        Layout.fillWidth: true
        Layout.alignment: Qt.AlignLeft | Qt.AlignTop

        GridLayout {
            id: userInput
            anchors.fill: parent
            transformOrigin: Item.Center
            Layout.fillWidth: true
            flow: Grid.LeftToRight
            rows: 2
            columns: 2

            Item {
                Layout.fillHeight: true
                Layout.fillWidth: true
                Layout.columnSpan: 2
                Rectangle {
                    id: rectangleText
                    anchors.fill: parent
                    color: backColour(model)
                    ColumnLayout {
                        id: instructionBox
                        anchors.fill: parent
                        spacing: 4
                        TextEdit {
                            id: instructionTitle
                            visible: (Boolean(model) && model.instructionTitle) ? true : false
                            Layout.preferredHeight: parent.height * proportion.header
                            Layout.minimumHeight: 0
                            Layout.maximumHeight: parent.height * proportion.header * 2
                            Layout.fillWidth: true
                            clip: true
                            text: model ? model.instructionTitle : ""
                            textFormat: Text.AutoText
                            font.pixelSize: parent.height * proportion.header * 0.9
                            wrapMode: TextEdit.Wrap
                            readOnly: true
                            selectByMouse: true
                        }
                        ScrollView {
                            Layout.fillHeight: true
                            Layout.fillWidth: true
                            TextArea {
                                id: userInstruct
                                text: model ? model.instructionText : ""
                                textFormat: Text.AutoText
                                font.pixelSize: instructionBox.height * proportion.textHeight
                                color: instructionTitle.color
                                leftPadding: instructionPadding(model)
                                rightPadding: instructionPadding(model)
                                topPadding: instructionPadding(model)
                                bottomPadding: instructionPadding(model)
                                wrapMode: TextArea.WordWrap
                                readOnly: true
                                selectByMouse: true
                            }
                        }
                    }
                }
            }

            Item {
                Layout.fillWidth: true
                Layout.preferredHeight: parent.height * proportion.control
                Layout.minimumHeight: 30
                Layout.maximumHeight: 100
                Button {
                    anchors.fill: parent
                    id: leftButton
                    text: model ? model.control.leftButton.text : ""
                    enabled: model ? model.control.leftButton.enabled : false
                    font.pixelSize: parent.height * 0.7
                    onClicked: {
                        onControlClick(model.control.leftButton.text)
                    }
                    contentItem: Text {
                        text: leftButton.text
                        font: leftButton.font
                        opacity: enabled ? 1.0 : 0.3
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                        elide: Text.ElideNone
                        clip: true
                    }
                }
            }

            Item {
                Layout.fillWidth: true
                Layout.preferredHeight: parent.height * proportion.control
                Layout.minimumHeight: 30
                Layout.maximumHeight: 100
                Button {
                    id: rightButton
                    anchors.fill: parent
                    text: model ? model.control.rightButton.text : ""
                    enabled: model ? model.control.rightButton.enabled : false
                    antialiasing: true
                    transformOrigin: Item.Right
                    checkable: false
                    checked: false
                    highlighted: true
                    font.pixelSize: parent.height * 0.7
                    onClicked: onControlClick(model.control.rightButton.text)
                    contentItem: Text {
                        text: rightButton.text
                        font: rightButton.font
                        opacity: enabled ? 1.0 : 0.3
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                        elide: Text.ElideNone
                        clip: true
                    }
                }
            }
        }
    }
    function onControlClick(control) {
        model.control.onControl(control)
    }
    function backColour(model) {
        var colour = rectangleBase.color
        if (Boolean(model) && model.instructionTitle === "ERROR" ) {
            colour = instructionWidget.color
        } else if (Boolean(model) && model.enabled && model.instructionText) {
            colour = instructionWidget.color
        }
        return (colour)
    }
    function instructionPadding(model) {
        var padding = 4
        if (Boolean(model) && model.enabled && model.instructionText) {
            var instruction = model.instructionText.toLowerCase()
            if (instruction.includes("html")) {
                padding = 0
            }
        }
        return (padding)
    }
    function controlEnabled() {
        return (model && (model.control.rightButton.enabled || model.control.leftButton.enabled))
    }
}
