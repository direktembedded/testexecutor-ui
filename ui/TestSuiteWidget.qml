/*
 * Copyright (c) 2020 Direkt, Australia
 * Licensed under BSD-3-Clause, refer LICENSE.txt
 */
import QtQuick 2.0
import QtQuick.Controls 2.3
import QtQuick.Layouts 1.3
import QtQuick.Window 2.10

Item {
    id: suite_container
    property var tswModel

    Frame {
        width: parent.width
        height: parent.height

        background: Rectangle {
            id: rectangle
            color: "transparent"
            border.width: 10
            border.color: "red"
            anchors.fill: parent
        }

        ColumnLayout {
            id: column
            anchors.fill: parent

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
                Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                // The Item wrapper is to allow TextField pointSize to reference the parents height.
                Layout.preferredHeight: parent.height * 0.04
                Layout.minimumHeight: parent.height * 0.04
                Layout.maximumHeight: parent.height * 0.04
                Layout.fillWidth: true
                Button {
                    id: control_button
                    width: parent.width / 2
                    height: parent.height * 0.8
                    text: ""
                    enabled: false
                    padding: 3
                    spacing: 3
                    anchors.horizontalCenter: parent.horizontalCenter
                    font.pointSize: parent.height * 0.5
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                    onClicked: {
                        // Set suite state to 'next' which is informing the model to change to the next state.
                        tswModel.testsuite.suitestate = "next"
                        // Now the model has changed it state, adjust the UI container's state (see below)
                        //suite_container.state = "next"
                    }
                }
            }
        }
    }
    state: tswModel.testsuite.suitestate
/*
    Binding {
        target: tswModel
        property: "suitestate"
        value: state
    }
*/
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
        },
        State {
            name: "ready"
            PropertyChanges { target: control_button; text: "Start"; enabled: true  }
            PropertyChanges { target: instructionWidget; enabled: true  }
            PropertyChanges { target: identifierWidget; enabled: false  }
        },
        State {
            name: "running"
            PropertyChanges { target: control_button; text: "Stop"; enabled: true  }
            PropertyChanges { target: instructionWidget; enabled: true  }
            PropertyChanges { target: identifierWidget; enabled: false  }
        },
        State {
            name: "starting"
            PropertyChanges { target: control_button; text: "Starting"; enabled: false }
            PropertyChanges { target: instructionWidget; enabled: false  }
        },
        State {
            name: "stopping"
            PropertyChanges { target: control_button; text: "Stopping"; enabled: false }
            PropertyChanges { target: instructionWidget; enabled: false  }
            PropertyChanges { target: identifierWidget; enabled: false  }
        },
        State {
            name: "stopped"
            PropertyChanges { target: control_button; text: "Stopped"; enabled: false }
            PropertyChanges { target: instructionWidget; enabled: false  }
            PropertyChanges { target: identifierWidget; enabled: true  }
        }
    ]
}

