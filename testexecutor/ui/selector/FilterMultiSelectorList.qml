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

Item {
    id: filterList
    width: 400
    height: 100
    clip: true
    property var filters
    property int viewableCount: -1
    property var itemConfig
    signal changed()

    Rectangle {
        id: filterRectangle
        anchors.fill: parent

        ListView {
            id: filterListView
            clip: true
            snapMode: ListView.NoSnap
            boundsBehavior: Flickable.StopAtBounds
            anchors.fill: parent
            delegate: FilterMultiSelectorItem {
                height: (filterList.viewableCount <= 0) ? (filterListView.height / filterListView.count) : (filterListView.height / viewableCount)
                width: parent.width
                filterItem: model.filter
                onChanged: filterList.changed()
            }
            model: filters
        }
    }
}

