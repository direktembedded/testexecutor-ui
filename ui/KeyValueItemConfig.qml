/*
 * A qml item which acts as the default configuration for the key value item widget.
 *
 * Copyright (c) 2020 Direkt, Australia
 * Licensed under BSD-3-Clause, refer LICENSE
 */
import QtQuick 2.0

Item {
    /*
     * Define the proportions for the widths of the test result items.
     * The feedback area is not defined and will fill any remaining area.
     */
    property var proportion: {
        "name": 0.3
        // value fill remaining space
    }
    property var color: "#605b5b"
    property var border: {"color": "#00000000"}
    property var name: {
        "color": "#00000000",
        "text": {"color": "#e5e2e2"},
        "border": {"color": "#00000000"},
    }
    property var value: {
        "color": "#ffffff",
        "border": {"color": "#b9e5e2e2"},
        "text": {"color": "black"}
    }
}