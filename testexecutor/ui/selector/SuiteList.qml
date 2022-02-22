/*
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
import QtQuick.Controls

ListView {
    id: view
    property var collapsed: ({})
    property var selected: ({})
    property var section_count: ({})
    property var indicators: {0:"⮞", 1:"⮟"}
    property var config: SuiteSelectorConfig{}
    property int viewableCount: config ? config.viewableCount : -1
    property int row_height: (viewableCount < 0) ? 30 : view.height / (view.viewableCount)
    clip: true

    signal sectionClick(string section, bool selected)

    delegate: TestDelegate {
        id: testDelegate
        expanded: view.isSectionExpanded(model.owner)
        config: view.config.row
        dynamic_height: view.row_height

        Connections {
            target: view
            function onSectionClick(section, selected) {
                if (model.owner === section) {
                    model.selected = selected
                }
            }
        }
        onTestClick: function(model) {
            testClicked(model)
        }
    }

    header: SelectorHeader {
        width: parent.width
        config: view.config ? view.config.header: ""
        height: row_height
        anchors {
            left: parent.left
            right: parent.right
        }
    }

    section {
        id: section_id
        property: "model.owner"
        criteria: ViewSection.FullString
        delegate: SectionDelegate {
            id: sectionDelegate
            anchors {
                left: parent.left
                right: parent.right
            }
            text: section
            indicator: getIndicator(section)
            count: getSectionCount(section)
            selected: getSectionCount(section) > 0
            config: view.config.section
            onExpandClick: view.toggleSection(section)
            onSectionClick: view.toggleSelected(section)
        }
    }

    ScrollBar.vertical: ScrollBar {}

    onCountChanged: {
        // If the count changed int the list view model, take the simple
        // approach and reset section count
        var new_count = Object.keys(section_count).length
        if (new_count > 0) {
            section_count = {}
            view.section_countChanged()
        }
    }

    function isSectionExpanded(section) {
        return !(section in collapsed);
    }
    function showSection(section) {
        delete collapsed[section]
        collapsedChanged()
    }
    function hideSection(section) {
        collapsed[section] = true
        collapsedChanged()
    }
    function toggleSection(section) {
        if (isSectionExpanded(section)) {
            hideSection(section)
        } else {
            showSection(section)
        }
    }
    function toggleSelected(section) {
        if (isSectionSelected(section) || model.selected_count(section) > 0) {
            delete selected[section]
        } else {
            selected[section] = true
        }
        view.sectionClick(section, isSectionSelected(section))
        section_count[section] = model.selected_count(section)
        section_countChanged()
    }
    function isSectionSelected(section) {
        return (section in selected);
    }
    function getIndicator(owner) {
        var ind = ""
        var indicators = view.indicators
        if (config) {
            indicators = config.indicators
        }
        var istate = view.isSectionExpanded(owner)
        if (istate) {
            ind = indicators[1]
        } else {
            ind = indicators[0]
        }
        return ind
    }
    function getSectionCount(section) {
        var count = 0;
        if (section && section_count[section]) {
            count = section_count[section]
        }
        return (count)
    }
    function testClicked(clicked) {
        section_count[clicked.owner] = model.selected_count(clicked.owner)
        section_countChanged()
    }
}
