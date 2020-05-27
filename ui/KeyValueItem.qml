/*
 * A generic key value item with a label for the 'name' and a value which can be a string or list of string.
 * The layout can be controlled using a configuration json string.
 * To override the default config set context property contextKeyValueItemConfig with the desired json string.
 *
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
    property var config: KeyValueItemConfig {}

    Binding {
        target: model.value
        property: "value"
        value: valueIsArray() ? comboControl.currentText : identifier.text
    }

    Rectangle {
        id: rectangle
        width: parent.width
        color: config.color
        border.width: 1
        border.color: config.border.color
        anchors.fill: parent

        RowLayout {
            id: row
            height: parent.height
            spacing: 1.5
            anchors.fill: parent

            Rectangle {
                id: keyLabelRectangle
                Layout.preferredWidth: parent.width * config.proportion.name
                color: config.name.color
                Layout.alignment: Qt.AlignLeft | Qt.AlignTop
                border.color: config.name.border.color
                border.width: 1
                Layout.fillHeight: true

                Text {
                    id: identifierName
                    color: config.name.text.color
                    text: value.label
                    verticalAlignment: Text.AlignVCenter
                    anchors.rightMargin: 2
                    anchors.fill: parent
                    font.pixelSize: parent.height * 0.7
                    minimumPixelSize: 10
                    elide: Text.ElideLeft
                    horizontalAlignment: Text.AlignRight
                    ToolTip {
                        visible: identifierName.truncated ? mouseArea.containsMouse : false
                        timeout: 3000
                        contentItem:
                            Column {
                                Text {
                                    text: identifierName.text
                                    font.pixelSize: identifier.height
                                    font.weight: Font.ExtraBold
                                }
                            }
                    }
                    MouseArea {
                        id: mouseArea
                        anchors.fill: parent
                        hoverEnabled: true
                    }
                }
            }

            Rectangle {
                id: valueRectangle
                Layout.fillHeight: true
                color: config.value.color
                Layout.fillWidth: true
                border.width: 1
                border.color: config.value.border.color
                ComboBox {
                    id: comboControl
                    anchors.fill: parent
                    font.pixelSize: parent.height * 0.7
                    model: possibles
                    visible: valueIsArray()
                    ToolTip.visible: hovered
                    ToolTip.text: currentText
                    ToolTip.timeout: 3000
                    delegate: ItemDelegate {
                        width: comboControl.width
                        contentItem: Text {
                            text: modelData
                            font: comboControl.font
                            elide: Text.ElideRight
                            verticalAlignment: Text.AlignVCenter
                        }
                        highlighted: comboControl.highlightedIndex === index
                    }
                    background: Rectangle {
                        border.width: 1
                        border.color: config.value.border.color
                    }
                }

                TextInput {
                    id: identifier
                    text: value.value
                    color: config.value.text.color
                    visible: !valueIsArray()
                    activeFocusOnPress: false
                    autoScroll: true
                    clip: true
                    font.pixelSize: parent.height / 1.2
                    anchors.rightMargin: 0
                    anchors.leftMargin: 3
                    anchors.fill: parent
                    ToolTip {
                        visible: parent.text ? identifierMouseArea.containsMouse : false
                        timeout: 3000
                        contentItem:
                            Column {
                                Text {
                                    text: identifier.text
                                    font.pixelSize: identifier.height
                                    font.weight: Font.ExtraBold
                                }
                            }
                    }
                    MouseArea {
                        id: identifierMouseArea
                        anchors.fill: parent
                        hoverEnabled: true
                    }
                }
            }
        }
    }

    Component.onCompleted: parseConfigStr()

    function valueIsArray() {
        return (possibles.length > 1) ? true : false;
    }
    function parseConfigStr() {
        if (typeof contextKeyValueItemConfig !== "undefined") {
            var json = JSON.parse(contextKeyValueItemConfig)
            keyValueItem.config = json
        }
    }
}

