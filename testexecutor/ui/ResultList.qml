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

Item {
    id: resultList
    width: 600
    clip: true
    property var results
    property int viewableCount: -1
    property var itemConfig
    property var color: "#e5e2e2"

    Rectangle {
        id: resultListRectangle
        color: color
        anchors.fill: parent

        ListView {
            id: resultListView
            spacing: 1
            snapMode: ListView.NoSnap
            boundsBehavior: Flickable.StopAtBounds
            currentIndex: results ? results.currentTestIndex : 0
            highlightFollowsCurrentItem: true
            anchors.fill: parent
            delegate: ResultItem {
                height: (viewableCount <= 0) ? (resultListView.height / resultListView.count) : (resultListView.height / viewableCount)
                Component.onCompleted: {
                    if (results.currentTestIndex === -1) {
                        resultListView.positionViewAtEnd();
                    }
                    if (resultList.itemConfig) {
                        config = resultList.itemConfig
                    }
                }
            }
            model: results
            ScrollBar.vertical: ScrollBar {}
        }
    }
}
