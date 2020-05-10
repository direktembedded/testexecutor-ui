/*
 * Copyright (c) 2020 Direkt, Australia
 * Licensed under BSD-3-Clause, refer LICENSE
 */
import QtQuick 2.4
import QtQuick.Controls 2.1

Item {
    width: 600
    //height: children.height
    clip: true
    property var results
    property int viewableCount: -1

    Rectangle {
        id: resultListRectangle
        //height: children.height
        color: "#e5e2e2"
        anchors.fill: parent

        //property var rectResults: parent.results
        ListView {
            id: resultListView
            spacing: 1
            //height: children.height
            snapMode: ListView.NoSnap
            boundsBehavior: Flickable.StopAtBounds
            anchors.fill: parent
            delegate: ResultItem {
                height: (viewableCount <= 0) ? (resultListView.height / resultListView.count) : (resultListView.height / viewableCount)
            }
            model: results
            ScrollBar.vertical: ScrollBar {}
        }
    }
}
