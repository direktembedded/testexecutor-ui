/*
 * Copyright (c) 2020 Direkt, Australia
 * Licensed under BSD-3-Clause, refer LICENSE
 */
import QtQuick 2.0
import QtQuick.Layouts 1.3
import QtQuick.Controls 2.3

Item {
    id: identificationWidget
    property string inputid
    property var identifiers
    property var color
    property var itemConfig

    ColumnLayout {
        id: identificationWidgetLayout
        anchors.fill: parent

        KeyValueList {
            id: identificationList
            keyvalues: identifiers
            Layout.fillHeight: true
            Layout.fillWidth: true
            color: identificationWidget.color
            itemConfig: identificationWidget.itemConfig
        }

        Item {
            // The Item wrapper is to allow TextField pixelSize to reference the parents height.
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
                font.pixelSize: parent.height * 0.7
                // onAccepted is called when 'return' is entered.
                onAccepted: {
                    if (identificationWidget.inputid === singleInputField.text) {
                        identificationWidget.inputid = ""
                    }
                    identificationWidget.inputid = singleInputField.text
                    singleInputField.text = ""
                }
            }
        }
    }
}

