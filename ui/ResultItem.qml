/*
 * Copyright (c) 2020 Direkt, Australia
 * Licensed under BSD-3-Clause, refer LICENSE.txt
 */
import QtQuick 2.4
import QtQuick.Layouts 1.3

Item {
    id: resultItem
    width: parent.width
    height: 40
    clip: true

    Rectangle {
        id: resultRectangle
        color: "#605b5b"
        border.width: 3
        border.color: "#00000000"
        anchors.fill: parent

        RowLayout {
            id: resultsRow
            spacing: 1.5
            anchors.fill: parent

            Rectangle {
                id: nameRectangle
                Layout.preferredWidth: parent.width * 0.2
                color: "#00000000"
                Layout.fillHeight: true
                border.width: 0
                border.color: "#00b63333"

                Text {
                    id: resultName
                    color: "#e5e2e2"
                    text: name
                    verticalAlignment: Text.AlignVCenter
                    font.pixelSize: parent.height / 1.2
                    anchors.rightMargin: 2
                    anchors.fill: parent
                    clip: false
                    horizontalAlignment: Text.AlignRight
                }
            }

            Rectangle {
                id: feedbackRectangle
                color: "#8e8a8a"
                border.color: "#b9e5e2e2"
                Layout.fillHeight: true
                Layout.fillWidth: true
                border.width: 0

                Text {
                    id: feedback
                    color: "#e5e2e2"
                    text: result
                    verticalAlignment: Text.AlignVCenter
                    clip: false
                    font.pixelSize: parent.height / 1.2
                    anchors.rightMargin: 0
                    anchors.leftMargin: 3
                    anchors.fill: parent
                }
            }

            Rectangle {
                id: timeRectangle
                Layout.preferredWidth: parent.width * 0.1
                Layout.maximumWidth: parent.width * 0.2
                color: "#00000000"
                Layout.fillHeight: true
                border.width: 0
                border.color: "#e5e2e2"
                Text {
                    id: timeProgress
                    color: "#e5e2e2"
                    text: duration
                    verticalAlignment: Text.AlignVCenter
                    horizontalAlignment: Text.AlignRight
                    font.pixelSize: parent.height / 1.2
                    anchors.rightMargin: 0
                    anchors.fill: parent
                    clip: false
                }
            }
        }
    }
}

