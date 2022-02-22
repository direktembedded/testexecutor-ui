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

Item {
    id: keyValueList
    width: 400
    clip: true
    property var keyvalues
    property int viewableCount: -1
    property var itemConfig

    Rectangle {
        id: keyValueRectangle
        anchors.fill: parent

        ListView {
            id: keyValueListView
            clip: true
            snapMode: ListView.NoSnap
            boundsBehavior: Flickable.StopAtBounds
            anchors.fill: parent
            delegate: KeyValueItem {
                height: (viewableCount <= 0) ? (keyValueListView.height / keyValueListView.count) : (keyValueListView.height / viewableCount)
                Component.onCompleted: {
                    if (keyValueList.itemConfig) {
                        config = keyValueList.itemConfig
                    }
                }
            }
            model: keyvalues
        }
    }
}
