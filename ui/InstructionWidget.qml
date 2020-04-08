/*
 * Copyright (c) 2020 Direkt, Australia
 * Licensed under BSD-3-Clause, refer LICENSE.txt
 */
import QtQuick 2.4
import QtQuick.Controls 2.3
import QtQuick.Layouts 1.3

Item {
    width: parent.width
    height: parent.height
    property var model

    Rectangle {
        id: rectangle1
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

            TextEdit {
                id: userInstruct
                text: "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\np, li { white-space: pre-wrap; }\n</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:24px; font-weight:400; font-style:normal;\">\n<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Feedback</p></body></html>"
                textFormat: Text.RichText
                Layout.fillHeight: true
                Layout.fillWidth: true
                Layout.columnSpan: 2
                font.pixelSize: height * 0.1
            }

            Item {
                Layout.fillWidth: true
                Layout.preferredHeight: parent.height * 0.02
                Layout.minimumHeight: 40
                Layout.maximumHeight: 60
                Button {
                    anchors.fill: parent
                    id: buttonCancel
                    text: "Cancel"
                    font.pointSize: parent.height * 0.5
                }
            }

            Item {
                Layout.fillWidth: true
                Layout.preferredHeight: parent.height * 0.02
                Layout.minimumHeight: 40
                Layout.maximumHeight: 60
                Button {
                    id: buttonOk
                    anchors.fill: parent
                    text: "Ok"
                    antialiasing: true
                    transformOrigin: Item.Right
                    checkable: false
                    checked: false
                    highlighted: true
                    font.pointSize: parent.height * 0.5
                }
            }
        }
    }
}
