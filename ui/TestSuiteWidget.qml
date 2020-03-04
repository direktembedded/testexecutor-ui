/*
 * Copyright (c) 2020 Direkt, Australia
 * Licensed under BSD-3-Clause, refer LICENSE.txt
 */
import QtQuick 2.0
import QtQuick.Controls 2.3
import QtQuick.Layouts 1.3
import QtQuick.Window 2.10

Item {
    id: container
    property var tswModel

    Frame {
        width: parent.width
        height: parent.height

        background: Rectangle {
            id: rectangle
            color: "transparent"
            border.width: 10
            border.color: "red"
            anchors.fill: parent
        }

        ColumnLayout {
            id: column
            anchors.fill: parent

            IdentificationWidget {
                id: identifierWidget
                Layout.maximumHeight: parent.height * 0.4
                Layout.minimumHeight: parent.height * 0.2
                Layout.alignment: Qt.AlignLeft | Qt.AlignTop
                clip: false
                Layout.fillWidth: true
            }

            InstructionWidget {
                Layout.minimumWidth: parent.width * 0.3
                Layout.preferredHeight: parent.height * 0.4
                clip: true
                Layout.fillHeight: true
                Layout.fillWidth: true
            }

            ResultList {
                results: tswModel.resultlist
                id: testList
                Layout.preferredHeight: parent.height * 0.3
                Layout.minimumHeight: parent.height * 0.2
                Layout.fillWidth: true
                Layout.alignment: Qt.AlignLeft | Qt.AlignTop
                transformOrigin: Item.Center
                clip: true
                viewableCount: 10 // Change this to get this from a 'test suite view config' model
            }
        }
    }
}

