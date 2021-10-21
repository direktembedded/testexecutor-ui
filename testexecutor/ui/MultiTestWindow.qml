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

import QtQuick 2.4
import QtQuick.Controls 2.1
import QtQuick.Dialogs 1.2

ApplicationWindow {
    id: application
    title: (app_model) ? app_model.title : "Test Executor"
    visible: true
    width: 1200
    height: 800
    visibility: "Maximized"
    MultiTestWidget {
        test_suites: model_list
    }
    onClosing: {
        if (model_list.active_suites) {
            close.accepted = false
            if (Boolean(app_model) && app_model.allowAbort) {
                activeSuitesDialog.open()
            } else {
                closeToolTip.open()
            }
        } else {
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
            text: (app_model) ? app_model.closeText : "Do you want to abort all tests?"
        }
        standardButtons: StandardButton.Yes | StandardButton.No
        onYes: {
            app_model.abortAll()
        }
    }
}

