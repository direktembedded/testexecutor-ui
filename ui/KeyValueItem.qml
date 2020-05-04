/*
 * Copyright (c) 2020 Direkt, Australia
 * Licensed under BSD-3-Clause, refer LICENSE
 */
import QtQuick 2.12
import QtQuick.Layouts 1.3
import QtQuick.Controls 2.12

Item {
    id: keyValueItem
    width:parent.width
    height: 40
    clip: true

    Rectangle {
        id: rectangle
        width: parent.width
        color: "#605b5b"
        border.color: "#00000000"
        anchors.fill: parent

        RowLayout {
            id: row
            height: parent.height
            anchors.fill: parent

            Rectangle {
                id: keyLabelRectangle
                Layout.preferredWidth: parent.width * 0.3
                color: "#00000000"
                Layout.alignment: Qt.AlignLeft | Qt.AlignTop
                border.color: "#00000000"
                Layout.fillHeight: true

                Text {
                    id: identifierName
                    color: "#e5e2e2"
                    text: label
                    verticalAlignment: Text.AlignVCenter
                    anchors.rightMargin: 2
                    anchors.fill: parent
                    font.pointSize: parent.height * 0.7
                    minimumPointSize: 10
                    clip: true
                    horizontalAlignment: Text.AlignRight
                }
            }

            Rectangle {
                id: valueRectangle
                Layout.fillHeight: true
                color: "#ffffff"
                Layout.fillWidth: true
                border.width: 1
                ComboBox {
                    id: comboControl
                    anchors.fill: parent
                    font.pointSize: parent.height * 0.5
                    model: value
                    visible: valueIsArray()
                    delegate: ItemDelegate {
                        width: comboControl.width
                        contentItem: Text {
                            text: modelData
                            font: comboControl.font
                            elide: Text.ElideRight
                            verticalAlignment: Text.AlignVCenter
                        }
                        highlighted: control.highlightedIndex === index
                    }
                    background: Rectangle {
                        border.width: 1
                    }
                }

                TextInput {
                    id: identifier
                    text: value
                    visible: !valueIsArray()
                    activeFocusOnPress: false
                    autoScroll: true
                    clip: true
                    font.pixelSize: parent.height / 1.2
                    anchors.rightMargin: 0
                    anchors.leftMargin: 3
                    anchors.fill: parent
                }
            }
        }
    }
    function valueIsArray() {
        return (value.length > 1) ? true : false;
    }
}

