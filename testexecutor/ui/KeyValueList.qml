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
