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

/*
 * A View for selection tests to run
 */

import QtQuick 2.4
import QtQuick.Controls 2.4
import QtQuick.Layouts 1.3


Item {
    id: suiteSelector
    property var config: SuiteSelectorConfig{}
    property var cntrlModel
    width: 640
    height: 480
    ColumnLayout {
        id: columnLayout
        anchors.fill: parent

        FilterMultiSelectorList {
            id: filterMultiSelectorList
            Layout.preferredHeight: parent.height * 0.07
            Layout.fillWidth: true
            filters: cntrlModel ? cntrlModel.filters : null
            itemConfig: suiteSelector.config ? suiteSelector.config.filter: ""
            onChanged: {}
        }

        SuiteList {
            id: suiteTree
            Layout.fillHeight: true
            Layout.fillWidth: true
            config: suiteSelector.config
            model: cntrlModel ? cntrlModel.testselector : null
        }

        ToolTip {
            visible: cntrlModel ? cntrlModel.errors : false
            timeout: 3000
            delay: 100
            contentItem:
                Column {
                    Text {
                        width: filterMultiSelectorList.width / 2
                        wrapMode: Text.Wrap
                        text: cntrlModel ? cntrlModel.errors : ""
                        font.pixelSize: filterMultiSelectorList.height * 0.3
                        font.weight: Font.ExtraBold
                        color: "red"
                    }
                }
        }
    }
}
