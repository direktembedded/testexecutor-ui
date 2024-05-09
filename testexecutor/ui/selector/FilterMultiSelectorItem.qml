/*
 * Copyright 2020 Sipke Vriend, Australia
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

/*
 * A View for selection tests to run
 */

import QtQuick
import QtQuick.Layouts
import QtQuick.Controls

Item {
    id: filterSelector
    property int viewableCount: 5
    property var filterItem
    property var tooltipText: "Select item to filter with"
    property var config: FilterMultiSelectorItemConfig{}
    signal changed()
    width: 600
    height: 30

    Frame {
        padding: 2
        width: parent.width
        height: parent.height

        RowLayout {
            anchors.fill: parent
            Rectangle {
                id: valueRectangle
                Layout.fillHeight: true
                Layout.preferredWidth: parent.width * 0.2
                Layout.minimumWidth: parent.width * 0.05
                Layout.maximumWidth: parent.width * 0.5
                color: Boolean(config) ? config.list.background.color : "lightgray"
                border.width: 1
                border.color: Boolean(config) ? config.list.border.color : "black"
                ComboBox {
                    id: comboControl
                    height: parent.height
                    wheelEnabled: true
                    //editable: true
                    width: parent.width
                    font.pixelSize: parent.height * 0.7
                    bottomPadding: height * 0.1
                    leftPadding: 2
                    rightPadding: 0
                    contentItem: Text {
                        leftPadding: 0
                        rightPadding: comboControl.indicator.width + comboControl.spacing
                        text: comboControl.displayText
                        font: comboControl.font
                        verticalAlignment: Text.AlignVCenter
                        elide: Text.ElideRight
                    }

                    ToolTip {
                        visible: comboControl.hovered
                        timeout: 3000
                        delay: 500
                        contentItem:
                            Column {
                                Text {
                                    text: filterSelector.tooltipText
                                    font.pixelSize: filterListRectangle.height * 0.7
                                    font.weight: Font.ExtraBold
                                }
                            }
                    }

                    textRole: "display"
                    delegate: ItemDelegate {
                        width: comboControl.width
                        contentItem: Text {
                            text: model.display
                            font: comboControl.font
                            elide: Text.ElideRight
                            verticalAlignment: Text.AlignVCenter
                            padding: 0
                        }
                        highlighted: comboControl.highlightedIndex === index
                    }

                    background: Rectangle {
                        border.width: 1
                        border.color: valueRectangle.border.color
                    }
                    model: filterItem.proposed
                    onActivated: {
                        var v = comboControl.currentText
                        if (v) {
                            //filterListView.model.insert(0, {text: v})
                            filterListView.model.prepend(v)
                        }
                    }
                }
            }
            Rectangle {
                id: filterListRectangle
                Layout.fillHeight: true
                color: Boolean(config) ? valueRectangle.color : "lightgray"
                Layout.fillWidth: true

                Text {
                    color: "#8e8a8a"
                    text: filterItem.name
                    font.pixelSize: parent.height * 0.7
                    font.weight: Font.Light
                    font.italic: true
                    verticalAlignment: Text.AlignVCenter
                    horizontalAlignment: Text.AlignHCenter
                    anchors.fill: parent
                }

                ListView {
                    id: filterListView
                    anchors.fill: parent
                    orientation: ListView.Horizontal
                    spacing: 1
                    snapMode: ListView.NoSnap
                    boundsBehavior: Flickable.StopAtBounds
                    //currentIndex: model ? model.currentTestIndex : 0
                    highlightFollowsCurrentItem: true
                    delegate: FilterItem {
                        height: filterListView.height
                        Component.onCompleted: {
                            if (model.currentTestIndex === -1) {
                                filterListView.positionViewAtEnd();
                            }
                            filterSelector.changed()
                        }
                        onRemove: function(index) {
                            filterListView.model.remove(index)
                            filterSelector.changed()
                        }
                        config: filterSelector.config.item
                    }
                    ScrollBar.horizontal: ScrollBar {
                        policy: ScrollBar.AsNeeded
                    }
                    model: filterItem.selected
                }
            }
        }
    }

    Component.onCompleted: parseConfigStr()

    function parseConfigStr() {
        if (typeof contextFilterSelectorItemConfig !== "undefined") {
            var json = JSON.parse(contextFilterSelectorItemConfig)
            filterSelector.config = json
        }
    }
}
