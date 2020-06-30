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
    property var color: "#e5e2e2"
    property var proportion: {"input", 0.15}
    property alias itemConfig: identificationList.itemConfig

    ColumnLayout {
        id: identificationWidgetLayout
        anchors.fill: parent

        KeyValueList {
            id: identificationList
            keyvalues: identifiers
            Layout.fillHeight: true
            Layout.fillWidth: true
        }

        Item {
            // The Item wrapper is to allow TextField pixelSize to reference the parents height.
            Layout.preferredHeight: parent.height * proportion.input
            Layout.minimumHeight: parent.height * 0.15
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
                // Whenever a new line is detected we want to update input it also so the caller gets the scanned input
                onTextEdited: {
                    var str = singleInputField.text
                    if (str.charAt(str.length - 1) === '\n') {
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
}

