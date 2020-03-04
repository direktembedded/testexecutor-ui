/*
 * Copyright (c) 2020 Direkt, Australia
 * Licensed under BSD-3-Clause, refer LICENSE.txt
 */
import QtQuick 2.4
import QtQuick.Window 2.10

Item {
    width: 800
    height: 800
    Row {
        id: suiteRows
        spacing: 5
        clip: false
        anchors.fill: parent
        Repeater {
            id: testSuiteRepeater
            anchors.fill: parent
            model: model_list
            delegate: TestSuiteWidget {
                tswModel: model
                width: parent.width / testSuiteRepeater.count
                height: parent.height
            }
        }
    }
}
