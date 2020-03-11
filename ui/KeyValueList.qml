/*
 * Copyright (c) 2020 Direkt, Australia
 * Licensed under BSD-3-Clause, refer LICENSE.txt
 */
import QtQuick 2.4

Item {
    width: 400
    clip: true
    property var keyvalues
    property int viewableCount: -1

    Rectangle {
        id: rectangle
        color: "#e5e2e2"
        anchors.fill: parent

        ListView {
            id: listView
            clip: true
            snapMode: ListView.NoSnap
            boundsBehavior: Flickable.StopAtBounds
            anchors.fill: parent
            delegate: KeyValueItem {
                height: (viewableCount <= 0) ? (listView.height / listView.count) : (listView.height / viewableCount)
            }
            model: keyvalues
        }
    }
}
