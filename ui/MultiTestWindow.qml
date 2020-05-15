import QtQuick 2.4
import QtQuick.Controls 2.1
import QtQuick.Dialogs 1.2

ApplicationWindow {
    id: application
    title: (app_model) ? app_model.title : "Test Executor"
    visible: true
    width: 800
    height: 800
    MultiTestWidget {
        test_suites: model_list
    }
    onClosing: {
        if (model_list.active_suites) {
            close.accepted = false
            if (Boolean(app_model) && app_model.allowAbort) {
                activeSuitesDialog.open()
            } else {
                closeToolTip.open()
            }
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
                    text: (app_model) ? app_model.closeHeading : "There Are Still Tests Running"
                    font.pointSize: application.height * 0.03
                    font.weight: Font.ExtraBold
                }
                Text {
                    text: (app_model) ? app_model.closeText : "Stop all suites if you want to quit"
                    font.pointSize: application.height * 0.02
                    font.weight: Font.ExtraBold
                }
            }
    }

    Dialog {
        id: activeSuitesDialog
        title: (app_model) ? app_model.closeHeading : "There Are Still Tests Running"
        Label {
            text: (app_model) ? app_model.closeText : "Do you want to abort all tests?"
        }
        standardButtons: StandardButton.Yes | StandardButton.No
        onYes: {
            app_model.abortAll()
        }
    }
}

