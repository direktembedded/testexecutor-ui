/*
 * Copyright (c) 2020 Direkt, Australia
 * Licensed under BSD-3-Clause, refer LICENSE file
 */
import QtQuick 2.4
import QtQuick.Controls 2.3
import QtQuick.Layouts 1.3

Item {
    id: instructionWidget
    width: parent.width
    height: parent.height
    property var color: "yellow"
    property var proportion: {"header": 0.1, "textHeight": 0.05, "control": 0.1}
    property var model

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
                    color: (Boolean(model) && model.enabled && model.instructionText) ? instructionWidget.color : rectangleBase.color
                    ColumnLayout {
                        id: instructionBox
                        anchors.fill: parent
                        spacing: 4
                        TextEdit {
                            id: instructionTitle
                            visible: (Boolean(model) && model.instructionTitle) ? true : false
                            Layout.preferredHeight: parent.height * proportion.header
                            Layout.minimumHeight: 0
                            Layout.maximumHeight: 60
                            text: model ? model.instructionTitle : ""
                            textFormat: Text.AutoText
                            font.pixelSize: parent.height * proportion.header * 0.9
                            wrapMode: TextEdit.WordWrap
                            enabled: false
                        }
                        ScrollView {
                            Layout.fillHeight: true
                            Layout.fillWidth: true
                            TextArea {
                                id: userInstruct
                                //text: "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\np, li { white-space: pre-wrap; }\n</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:24px; font-weight:400; font-style:normal;\">\n<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Feedback</p></body></html>"
                                text: model ? model.instructionText : ""
                                textFormat: Text.AutoText
                                font.pixelSize: instructionBox.height * proportion.textHeight
                                color: instructionTitle.color
                                wrapMode: TextEdit.WordWrap
                                enabled: false
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
}
