/*
 * Copyright (c) 2020 Direkt, Australia
 * Licensed under BSD-3-Clause, refer LICENSE
 */
import QtQuick 2.4

Item {
    id: keyValueList
    width: 400
    clip: true
    property var keyvalues
    property int viewableCount: -1
    property var color: "#e5e2e2"
    property var itemConfig

    Rectangle {
        id: keyValueRectangle
        color: keyValueList.color
        anchors.fill: parent

        ListView {
            id: listView
            clip: true
            snapMode: ListView.NoSnap
            boundsBehavior: Flickable.StopAtBounds
            anchors.fill: parent
            delegate: KeyValueItem {
                height: (viewableCount <= 0) ? (listView.height / listView.count) : (listView.height / viewableCount)
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
