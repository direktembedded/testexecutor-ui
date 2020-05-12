/*
 * Copyright (c) 2020 Direkt, Australia
 * Licensed under BSD-3-Clause, refer LICENSE
 */
import QtQuick 2.0
import QtQuick.Controls 2.3
import QtQuick.Layouts 1.3
import QtQuick.Window 2.10

Item {
    id: suite_container
    property var tswModel
    property int duration

    Frame {
        bottomPadding: 8
        padding: 4
        anchors.fill: parent

        background: Rectangle {
            id: frameRectangle
            color: "transparent"
            anchors.fill: parent
        }

        ColumnLayout {
            id: testSuiteColumn
            anchors.fill: parent

            Rectangle {
                id: rectangleTitle
                Layout.maximumHeight: parent.height * 0.1
                Layout.minimumHeight: parent.height * 0.04
                Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                Layout.fillWidth: true
                color: frameRectangle.color

                Text {
                    id: suiteTitle
                    text: tswModel.testsuite.title
                    font.weight: Font.ExtraBold
                    anchors.fill: parent
                    horizontalAlignment: Text.AlignHCenter
                    font.pixelSize: parent.height * 0.7
                    font.bold: true
                    font.family: "Arial"
                    clip: true
                }
            }

            IdentificationWidget {
                id: identifierWidget
                Layout.maximumHeight: parent.height * 0.4
                Layout.minimumHeight: parent.height * 0.2
                Layout.alignment: Qt.AlignLeft | Qt.AlignTop
                clip: false
                Layout.fillWidth: true
                Binding {
                    target: tswModel.testsuite
                    property: "newid"
                    value: identifierWidget.inputid
                }
                identifiers: tswModel.testsuite.identifiers
            }

            InstructionWidget {
                id: instructionWidget
                Layout.minimumWidth: parent.width * 0.3
                Layout.preferredHeight: parent.height * 0.4
                clip: true
                Layout.fillHeight: true
                Layout.fillWidth: true
                model: tswModel.testsuite.instructions
            }

            ResultList {
                results: tswModel.testsuite.results
                id: testList
                Layout.preferredHeight: parent.height * 0.3
                Layout.minimumHeight: parent.height * 0.2
                Layout.fillWidth: true
                Layout.alignment: Qt.AlignLeft | Qt.AlignTop
                transformOrigin: Item.Center
                clip: true
                viewableCount: 10 // Change this to get this from a 'test suite view config' model
            }
            Item {
                id: buttonContainer
                Layout.fillHeight: true
                Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                // The Item wrapper is to allow TextField pixelSize to reference the parents height.
                Layout.preferredHeight: parent.height * 0.04
                Layout.minimumHeight: parent.height * 0.04
                Layout.maximumHeight: parent.height * 0.04
                Layout.fillWidth: true
                GridLayout {
                    anchors.fill: parent
                    columns: 5
                    rows: 1
                    Button {
                        id: control_button
                        width: parent.width
                        height: parent.height * 0.8
                        text: ""
                        Layout.column: 3
                        Layout.columnSpan: 1
                        enabled: false
                        padding: 0
                        spacing: 3
                        anchors.horizontalCenter: parent.horizontalCenter
                        font.pixelSize: parent.height * 0.7
                        onClicked: {
                            // Set suite state to 'next' which is informing the model to change to the next state.
                            tswModel.testsuite.suitestate = "next"
                        }
                        contentItem: Text {
                            text: control_button.text
                            font: control_button.font
                            opacity: enabled ? 1.0 : 0.3
                            //color: control_button.down ? "#17a81a" : "#21be2b"
                            horizontalAlignment: Text.AlignHCenter
                            verticalAlignment: Text.AlignVCenter
                            elide: Text.ElideNone
                            clip: true
                        }
                    }
                    Timer {
                        interval: 1000;
                        running: state === "running" || state === "stopping";
                        repeat: true
                        onTriggered: {
                            duration = duration + 1
                        }
                    }
                    Text {
                        id: suiteProgress
                        color: "#e5e2e2"
                        text: formatTime(duration)
                        Layout.fillWidth: true
                        Layout.column: 5
                        Layout.alignment: Qt.AlignRight | Qt.AlignVCenter
                        verticalAlignment: Text.AlignVCenter
                        horizontalAlignment: Text.AlignRight
                        font.pixelSize: parent.height / 1.2
                        anchors.rightMargin: 0
                        clip: true
                    }
                }
            }
        }
    }
    state: tswModel.testsuite.suitestate

    states: [
        State {
            name: "next"
            PropertyChanges { target: control_button; text: "next"; enabled: false  }
            PropertyChanges { target: instructionWidget; enabled: false  }
            PropertyChanges { target: identifierWidget; enabled: false  }
        },
        State {
            name: "idle"
            PropertyChanges { target: control_button; text: "Idle"; enabled: false  }
            PropertyChanges { target: instructionWidget; enabled: false  }
            PropertyChanges { target: identifierWidget; enabled: true  }
            PropertyChanges { target: frameRectangle; color: suiteResultColour() }
            PropertyChanges { target: suite_container; duration: 0 }
        },
        State {
            name: "ready"
            PropertyChanges { target: control_button; text: "Clear"; enabled: true  }
            PropertyChanges { target: instructionWidget; enabled: true  }
            PropertyChanges { target: identifierWidget; enabled: true  }
            PropertyChanges { target: frameRectangle; color: "gray" }
        },
        State {
            name: "running"
            PropertyChanges { target: control_button; text: "Stop"; enabled: true  }
            PropertyChanges { target: instructionWidget; enabled: true  }
            PropertyChanges { target: identifierWidget; enabled: false  }
            PropertyChanges { target: frameRectangle; color: "gray" }
        },
        State {
            name: "starting"
            PropertyChanges { target: control_button; text: "Starting"; enabled: false }
            PropertyChanges { target: instructionWidget; enabled: false  }
            PropertyChanges { target: frameRectangle; color: "gray" }
        },
        State {
            name: "stopping"
            PropertyChanges { target: control_button; text: "Stopping"; enabled: false }
            PropertyChanges { target: instructionWidget; enabled: true  }
            PropertyChanges { target: identifierWidget; enabled: false  }
            PropertyChanges { target: frameRectangle; color: "orange" }
        },
        State {
            name: "stopped"
            PropertyChanges { target: control_button; text: "Clear"; enabled: true }
            PropertyChanges { target: instructionWidget; enabled: false  }
            PropertyChanges { target: identifierWidget; enabled: true  }
            PropertyChanges { target: frameRectangle; color: "orange" }
        },
        State {
            name: "end"
            PropertyChanges { target: control_button; text: "Clear"; enabled: true }
            PropertyChanges { target: instructionWidget; enabled: false  }
            PropertyChanges { target: identifierWidget; enabled: true  }
            PropertyChanges { target: frameRectangle; color: suiteResultColour() }
        }
    ]
    function suiteResultColour()
    {
        var colour = "lightgray";
        if (tswModel.testsuite.result === "Pass")
        {
            colour = "green"
        }
        else if (tswModel.testsuite.result === "Fail")
        {
            colour = "red"
        }
        return colour;
    }
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
