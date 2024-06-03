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
import QtQuick.Layouts
import QtQuick.Controls

Item {
    id: resultItem
    width: parent ? parent.width : 100
    height: 40
    clip: true
    property var config: ResultItemConfig{}

    Rectangle {
        id: resultRectangle
        color: config.color
        border.width: 3
        border.color: config.border.color
        anchors.fill: parent

        RowLayout {
            id: resultsRow
            spacing: 1.5
            anchors.fill: parent

            Rectangle {
                id: nameRectangle
                Layout.preferredWidth: parent.width * config.proportion.name
                color: config.name.color
                Layout.fillHeight: true

                Text {
                    id: resultName
                    color: config.name.text.color
                    text: Boolean(test) ? test.name : ""
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
                color: config.feedback.color
                border.color: config.feedback.border.color
                Layout.fillHeight: true
                Layout.fillWidth: true
                Rectangle {
                    height: parent.height
                    width: Boolean(test) ? parent.width * test.progress : 0
                    color: Boolean(test) && test.progress === 1 ? "transparent" : config.feedback.progress.color
                    opacity: 0.5
                }
                Text {
                    id: feedback
                    color: Boolean(test) && test.progress < 1 ? config.feedback.text.color.default : config.feedback.text.color.progress
                    text: Boolean(test) ? test.feedback : ""
                    verticalAlignment: Text.AlignTop
                    clip: true
                    font.pixelSize: parent.height / 1.2
                    anchors.rightMargin: 0
                    anchors.leftMargin: 3
                    anchors.fill: parent
                }
            }

            Rectangle {
                id: timeRectangle
                Layout.preferredWidth: parent.width * config.proportion.time
                Layout.maximumWidth: parent.width * 0.3
                color: config.time.color
                Layout.fillHeight: true
                Timer {
                    interval: 1000
                    running: (state === "Running") && Boolean(test) && (test.progress < 1)
                    repeat: true
                    onTriggered: {
                        test.duration = test.duration + 1
                    }
                }
                Text {
                    id: timeProgress
                    color: config.time.text.color
                    text: Boolean(test) ? formatTime(test.duration) : ""
                    verticalAlignment: Text.AlignVCenter
                    horizontalAlignment: Text.AlignRight
                    font.pixelSize: parent.height / 1.2
                    anchors.rightMargin: 0
                    anchors.fill: parent
                    clip: true
                }
            }
        }
        ToolTip {
            visible: test && test.name ? resultMouseArea.containsMouse : false
            timeout: 3000
            delay: 500
            contentItem:
                Row {
                    Rectangle {
                        Text {
                            text: resultName.text
                            font.pixelSize: resultRectangle.height
                            font.weight: Font.Bold
                            color: resultName.color
                            rightPadding: 5
                            leftPadding: 10
                        }
                        color: nameRectangle.color
                        width: childrenRect.width
                        height: childrenRect.height
                    }
                    Rectangle {
                        Text {
                            text: feedback.text ? feedback.text:"  "
                            font.pixelSize: resultRectangle.height
                            font.weight: Font.Bold
                            color: feedback.color
                            rightPadding: 5
                            leftPadding: 5
                        }
                        color: feedbackRectangle.color
                        width: childrenRect.width
                        height: childrenRect.height
                    }
                    Rectangle {
                        Text {
                            text: timeProgress.text
                            font.pixelSize: resultRectangle.height
                            font.weight: Font.Bold
                            color: timeProgress.color
                            rightPadding: 10
                            leftPadding: 5
                        }
                        color: timeRectangle.color
                        width: childrenRect.width
                        height: childrenRect.height
                    }
                }
        }
        MouseArea {
            id: resultMouseArea
            anchors.fill: parent
            hoverEnabled: true
        }
    }
    state: test ? test.result : "Running"
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

