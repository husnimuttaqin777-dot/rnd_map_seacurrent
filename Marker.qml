import QtQuick 2.0
import QtLocation 5.11

MapQuickItem {
    id: marker
    property alias text: txt.text
    sourceItem: Rectangle {
        width: 30
        height: 30
        color: "transparent"
        Image {
            anchors.fill: parent
            source: "drone.png" // Ignore warnings from this
            sourceSize: Qt.size(parent.width, parent.height)
        }
        Text {
            id: txt
            anchors.fill: parent
        }
    }
    opacity: 1.0
    anchorPoint: Qt.point(sourceItem.width/2, sourceItem.height/2)
}