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
import QtQuick.Layouts

Rectangle {
    property var proportion: {"name": 0.15}
    property var config: HeaderConfig{}
    height: 30
    width: parent.width
    color: config ? config.color.default : "lightgray"
    RowLayout {
        anchors.fill: parent
        Text {
            Layout.fillHeight: true
            Layout.preferredWidth: parent.width * (proportion ? proportion.name : 0.15)
            text: config ? config.name : "Test"
            font.pixelSize: parent.height / 1.3
            color: config ? config.text.color: "black"
        }
        Text {
            Layout.fillHeight: true
            Layout.fillWidth: true
            text: config ? config.description : "Description"
            font.pixelSize: parent.height / 1.3
            color: config ? config.text.color: "black"
        }
    }
}
