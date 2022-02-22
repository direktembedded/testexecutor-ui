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
    id: identificationWidget
    property string inputid
    property var identifiers
    property var color: "#e5e2e2"
    property var proportion: {"input": 0.15}
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
            Layout.maximumHeight: parent.height
            Layout.fillWidth: true

            TextField {
                id: singleInputField
                text: ""
                topPadding: 0
                bottomPadding: 0
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

