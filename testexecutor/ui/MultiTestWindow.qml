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
import QtQuick.Dialogs

ApplicationWindow {
    id: application
    title: (app_model) ? app_model.title : "Test Executor"
    visible: true
    width: 1200
    height: 800
    visibility: (app_model && app_model.visibility) ? app_model.visibility : "Maximized"
    MultiTestWidget {
        test_suites: model_list
    }
    onClosing: function(close) {
        if (model_list.active_suites) {
            close.accepted = false
            if (Boolean(app_model) && app_model.allowAbort) {
                activeSuitesDialog.open()
            } else {
                closeToolTip.open()
            }
        } else {
            app_model.abortAll(true)
            close.accepted = true
        }
    }

    ToolTip {
        id: closeToolTip
        timeout: 2000
        background: Rectangle {
            border.color: "red"
            color: "yellow"
        }
        contentItem:
            Column {
                Text {
                    text: (app_model) ? app_model.closeHeading : "There Are Still Tests Running"
                    font.pixelSize: application.height * 0.03
                    font.weight: Font.ExtraBold
                }
                Text {
                    text: (app_model) ? app_model.closeText : "Stop all suites if you want to quit"
                    font.pixelSize: application.height * 0.03
                    font.weight: Font.ExtraBold
                }
            }
    }

    Dialog {
        id: activeSuitesDialog
        title: (app_model) ? app_model.closeHeading : "There Are Still Tests Running"
        Label {
            id: label
            text: (app_model) ? app_model.closeText : "Do you want to abort all tests?"
            font.pixelSize: application.width * 0.02 > 11 ? application.width * 0.02:11
        }
        font.pixelSize: application.width * 0.02 > 11 ? application.width * 0.02:11
        standardButtons: Dialog.Yes | Dialog.No
        onAccepted: {
            app_model.abortAll(false)
            app_model.abortAll(false)
        }
        width: label.width * 1.05
        x: (parent.width - width) / 2
        y: (parent.height - height) / 2
        implicitWidth: width
    }
}

