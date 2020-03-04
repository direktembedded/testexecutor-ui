/*
 * Copyright (c) 2020 Direkt, Australia
 * Licensed under BSD-3-Clause, refer LICENSE.txt
 */
import QtQuick 2.0
import QtQuick.Layouts 1.3
import QtQuick.Controls 2.3

Item {
    id: identificationWidget
    property string inputid
    ColumnLayout {
        id: identificationWidgetLayout
        anchors.fill: parent

        KeyValueList {
            id: identificationList
            Layout.fillHeight: true
            Layout.fillWidth: true
        }

        Item {
            // The Item wrapper is to allow TextField pointSize to reference the parents height.
            Layout.preferredHeight: parent.height * 0.2
            Layout.minimumHeight: parent.height * 0.1
            Layout.maximumHeight: parent.height * 0.3
            Layout.fillWidth: true
            TextField {
                id: singleInputField
                text: ""
                anchors.fill: parent
                horizontalAlignment: Text.AlignHCenter
                placeholderText: "Input"
                font.pointSize: parent.height * 0.5
                onAccepted: {
                    identificationWidget.inputid = singleInputField.text
                    singleInputField.text = ""
                }
            }
        }
    }
}

