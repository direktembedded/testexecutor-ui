/*
 * Copyright (c) 2020 Direkt, Australia
 * Licensed under BSD-3-Clause, refer LICENSE
 */
import QtQuick 2.4
import QtQuick.Controls 2.3
import QtQuick.Layouts 1.3
import QtQuick.Window 2.10
import QtQuick.Dialogs 1.2

Item {
    id: suite_container
    property var tswModel
    property int duration
    property var config: TestSuiteConfig{}

    Frame {
        bottomPadding: 8
        padding: 4
        width: parent.width
        height: parent.height

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
                Layout.maximumHeight: parent.height * config.proportion.title
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
                    font.pixelSize: parent.height
                    font.bold: true
                    font.family: "Arial"
                    clip: true
                }
            }

            IdentificationWidget {
                id: identifierWidget
                Layout.maximumHeight: parent.height * 0.5
                Layout.preferredHeight: parent.height * (config ? config.proportion.identification : 0.3)
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
                color: config ? config.identification.color : "#e5e2e2"
                proportion: config ? config.identification.proportion : ""
                itemConfig: config ? config.identification.item : ""
            }

            InstructionWidget {
                id: instructionWidget
                Layout.minimumHeight: parent.height * 0.3
                Layout.preferredHeight: parent.height * config.proportion.instructions
                Layout.maximumHeight: parent.height * 0.7
                clip: true
                Layout.fillWidth: true
                model: tswModel.testsuite.instructions
            }

            ResultList {
                results: tswModel.testsuite.results
                id: testList
                Layout.fillWidth: true
                Layout.fillHeight: true
                Layout.alignment: Qt.AlignLeft | Qt.AlignTop
                transformOrigin: Item.Center
                clip: true
                viewableCount: config.results.viewableCount
                color: config.results.color
                itemConfig: config.results.item
            }
            Item {
                id: buttonContainer
                Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                // The Item wrapper is to allow TextField pixelSize to reference the parents height.
                Layout.preferredHeight: parent.height * config.proportion.status
                Layout.minimumHeight: parent.height * config.proportion.status
                Layout.maximumHeight: parent.height * config.proportion.status
                Layout.fillWidth: true
                GridLayout {
                    anchors.fill: parent
                    columns: 3
                    rows: 1
                    Button {
                        id: control_button
                        width: parent.width
                        height: parent.height * 0.8
                        text: ""
                        Layout.column: 2
                        Layout.columnSpan: 1
                        enabled: false
                        padding: 0
                        spacing: 3
                        font.pixelSize: parent.height * 0.7
                        onClicked: {
                            /*
                             * Call the action 'event' on the test suite model with the text of the button as defined
                             * in the configuration
                             */
                            if (suite_container.state === "running" || suite_container.state === "starting") {
                                actionDialog.action = control_button.text
                                actionDialog.open()
                            } else {
                                tswModel.testsuite.action(control_button.text)
                            }
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
                        Layout.fillWidth: false
                        Layout.column: 3
                        Layout.alignment: Qt.AlignRight | Qt.AlignVCenter
                        Layout.columnSpan: 1
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
            name: "idle"
            PropertyChanges { target: control_button; text: config.states.idle.button.text; enabled: true  }
            PropertyChanges { target: instructionWidget; enabled: false  }
            PropertyChanges { target: identifierWidget; enabled: true  }
            PropertyChanges { target: frameRectangle; color: suiteResultColour(config.states.idle.color.default) }
            PropertyChanges { target: suite_container; duration: 0 }
        },
        State {
            name: "ready"
            PropertyChanges { target: control_button; text: config.states.ready.button.text; enabled: true  }
            PropertyChanges { target: instructionWidget; enabled: true  }
            PropertyChanges { target: identifierWidget; enabled: true  }
            PropertyChanges { target: frameRectangle; color: config.states.ready.color }
        },
        State {
            name: "running"
            PropertyChanges { target: control_button; text: config.states.running.button.text; enabled: true  }
            PropertyChanges { target: instructionWidget; enabled: true  }
            PropertyChanges { target: identifierWidget; enabled: false  }
            PropertyChanges { target: frameRectangle; color: config.states.running.color }
        },
        State {
            name: "starting"
            PropertyChanges { target: control_button; text: config.states.running.button.text; enabled: false }
            PropertyChanges { target: instructionWidget; enabled: false  }
            PropertyChanges { target: frameRectangle; color: config.states.running.color }
        },
        State {
            name: "stopping"
            PropertyChanges { target: control_button; text: config.states.stopped.button.text; enabled: false }
            PropertyChanges { target: instructionWidget; enabled: true  }
            PropertyChanges { target: identifierWidget; enabled: false  }
            PropertyChanges { target: frameRectangle; color: config.states.stopped.color }
        },
        State {
            name: "stopped"
            PropertyChanges { target: control_button; text: config.states.stopped.button.text; enabled: true }
            PropertyChanges { target: instructionWidget; enabled: false  }
            PropertyChanges { target: identifierWidget; enabled: true  }
            PropertyChanges { target: frameRectangle; color: config.states.stopped.color }
        },
        State {
            name: "end"
            PropertyChanges { target: control_button; text: config.states.idle.button.text; enabled: true }
            PropertyChanges { target: instructionWidget; enabled: false  }
            PropertyChanges { target: identifierWidget; enabled: true  }
            PropertyChanges { target: frameRectangle; color: suiteResultColour(config.states.idle.color.default) }
        }
    ]

    Dialog {
        id: actionDialog
        property var action
        title: "There Are Tests Running"
        Label {
            text: "Do you want to " + control_button.text + "?"
        }
        standardButtons: StandardButton.Yes | StandardButton.No
        onYes: {
            tswModel.testsuite.action(action)
        }
    }

    function suiteResultColour(defaultColor)
    {
        var colour = defaultColor;
        if (tswModel.testsuite.result === "Pass")
        {
            colour = config.states.idle.color.pass
        }
        else if (tswModel.testsuite.result === "Fail")
        {
            colour = config.states.idle.color.fail
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
