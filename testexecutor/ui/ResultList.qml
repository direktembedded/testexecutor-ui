/*
 * Copyright (c) 2020 Direkt, Australia
 * Licensed under BSD-3-Clause, refer LICENSE
 */
import QtQuick 2.4
import QtQuick.Controls 2.1

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
