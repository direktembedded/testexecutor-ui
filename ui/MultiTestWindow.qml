import QtQuick 2.4
import QtQuick.Controls 2.1
import QtQuick.Dialogs 1.2

ApplicationWindow {
    id: application
    title: "Test Executor"
    visible: true
    width: 800
    height: 800
    MultiTestWidget {
        test_suites: model_list
    }
    onClosing: {
        if (model_list.active_suites) {
            close.accepted = false
            //activeSuitesDialog.open()
            closeToolTip.open()
        } else {
            close.accepted = true
        }
    }

    ToolTip {
        id: closeToolTip
        timeout: 2000
        background: Rectangle {
            border.color: "red"
            color: "yellow"
        }
        contentItem:
            Column {
                Text {
                    text: "There Are Still Tests Running"
                    font.pointSize: application.height * 0.03
                    font.weight: Font.ExtraBold
                }
                Text {
                    text: "Stop all suites if you want to quit"
                    font.pointSize: application.height * 0.02
                    font.weight: Font.ExtraBold
                }
            }

    }

    Dialog {
        id: activeSuitesDialog
        title: "Test Running"
        Label {
            text: "Please stop all tests before exiting"
        }
        standardButtons: StandardButton.Ok
    }
}

