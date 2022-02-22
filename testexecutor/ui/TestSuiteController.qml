/*
 * Copyright 2020 Sipke Vriend, Australia
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
import QtQuick.Layouts
import QtQuick.Window
import QtQuick.Dialogs
import "./selector"

Item {
    id: testSuiteController
    property alias tswModel: testSuiteWidget.tswModel
    property alias cntrlModel: suiteSelector.cntrlModel
    property alias duration: testSuiteWidget.duration
    property alias config: testSuiteWidget.config
    property alias about: testSuiteWidget.about
    property alias controllerConfig: suiteSelector.config
    property var useController: tswModel && Boolean(tswModel.testsuite.controller)
    width: 600
    height: 600
    RowLayout {
        id: rowLayout
        anchors.fill: parent

        SuiteSelector {
            id: suiteSelector
            Layout.fillHeight: true
            Layout.fillWidth: true
            visible: useController
        }
        TestSuiteWidget {
            id: testSuiteWidget
            Layout.minimumWidth: 0
            Layout.preferredWidth:  useController ? parent.width * 0.5 : parent.width
            Layout.maximumWidth:  useController ? 400 : parent.width
            Layout.fillHeight: true
        }
    }
}
