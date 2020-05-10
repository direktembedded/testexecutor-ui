/*
 * Copyright (c) 2020 Direkt, Australia
 * Licensed under BSD-3-Clause, refer LICENSE
 */
import QtQuick 2.4
import QtQuick.Layouts 1.3

Item {
    id: resultItem
    width: parent.width
    height: 40
    clip: true

    Rectangle {
        id: resultRectangle
        color: "#605b5b"
        border.width: 3
        border.color: "#00000000"
        anchors.fill: parent

        RowLayout {
            id: resultsRow
            spacing: 1.5
            anchors.fill: parent

            Rectangle {
                id: nameRectangle
                Layout.preferredWidth: parent.width * 0.2
                color: "#00000000"
                Layout.fillHeight: true
                border.width: 0
                border.color: "#00b63333"

                Text {
                    id: resultName
                    color: "#e5e2e2"
                    text: test.name
                    verticalAlignment: Text.AlignVCenter
                    font.pixelSize: parent.height / 1.2
                    anchors.rightMargin: 2
                    anchors.fill: parent
                    clip: false
                    horizontalAlignment: Text.AlignRight
                }
            }

            Rectangle {
                id: feedbackRectangle
                color: "#8e8a8a"
                border.color: "#b9e5e2e2"
                Layout.fillHeight: true
                Layout.fillWidth: true
                Rectangle {
                    height: parent.height
                    width: parent.width * test.progress
                    color: test.progress == 1 ? "transparent" : "green"
                    opacity: 0.5
                }
                Text {
                    id: feedback
                    color: "#e5e2e2"
                    text: test.feedback
                    verticalAlignment: Text.AlignVCenter
                    clip: true
                    font.pixelSize: parent.height / 1.2
                    anchors.rightMargin: 0
                    anchors.leftMargin: 3
                    anchors.fill: parent
                }
            }

            Rectangle {
                id: timeRectangle
                Layout.preferredWidth: parent.width * 0.2
                Layout.maximumWidth: parent.width * 0.3
                color: "#00000000"
                Layout.fillHeight: true
                border.width: 0
                border.color: "#e5e2e2"
                Timer {
                    interval: 1000;
                    running: (state === "Running") && (test.progress < 1);
                    repeat: true
                    onTriggered: {
                        test.duration = test.duration + 1
                    }
                }
                Text {
                    id: timeProgress
                    color: "#e5e2e2"
                    text: formatTime(test.duration)
                    verticalAlignment: Text.AlignVCenter
                    horizontalAlignment: Text.AlignRight
                    font.pixelSize: parent.height / 1.2
                    anchors.rightMargin: 0
                    anchors.fill: parent
                    clip: true
                }
            }
        }
    }
    state: test.result
    states: [
        State {
            name: "Running"
            PropertyChanges { target: feedbackRectangle; color: "#e5e2e2"  }
        },
        State {
            name: "Pass"
            PropertyChanges { target: feedbackRectangle; color: "green"  }
        },
        State {
            name: "Fail"
            PropertyChanges { target: feedbackRectangle; color: "red"  }
        }
    ]

    function formatTime(timeInSeconds) {
        var pad = function(num, size) { return ('000' + num).slice(size * -1); },
        time = parseFloat(timeInSeconds).toFixed(3),
        hours = Math.floor(time / 60 / 60),
        minutes = Math.floor(time / 60) % 60,
        seconds = Math.floor(time - minutes * 60),
        milliseconds = time.slice(-3);

        var s = pad(seconds, 2);
        if (timeInSeconds >= 60*60) {
            s = pad(hours, 2) + ':' + pad(minutes, 2) + ':' + pad(seconds, 2)
        } else if (timeInSeconds >= 60){
            s = pad(minutes, 2) + ':' + pad(seconds, 2)
        }

        return s;
    }
}

