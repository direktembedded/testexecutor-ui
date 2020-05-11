/*
 * Copyright (c) 2020 Direkt, Australia
 * Licensed under BSD-3-Clause, refer LICENSE
 */
import QtQuick 2.4

Item {
    property var test_suites
    anchors.fill: parent
    Row {
        id: suiteRows
        spacing: 2
        clip: false
        anchors.fill: parent
        Repeater {
            id: testSuiteRepeater
            anchors.fill: parent
            model: test_suites
            delegate: TestSuiteWidget {
                tswModel: model
                width: parent.width / testSuiteRepeater.count - 1
                height: parent.height
            }
        }
    }
}
