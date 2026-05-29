import QtQuick 2.15
import QtQuick.Window 2.15
import QtLocation 5.15
import QtPositioning 5.15

Window {
    visible: true
    width: 800
    height: 600
    title: "Sea Current Area Map"

    ListModel {
        id: currentModel
        ListElement { lat: 0.5270; lon: 103.2680; dir: 20  }
        ListElement { lat: 0.5275; lon: 103.2690; dir: 45  }
        ListElement { lat: 0.5280; lon: 103.2700; dir: 70  }
        ListElement { lat: 0.5285; lon: 103.2710; dir: 90  }
        ListElement { lat: 0.5290; lon: 103.2720; dir: 120 }
        ListElement { lat: 0.5265; lon: 103.2685; dir: 160 }
        ListElement { lat: 0.5270; lon: 103.2695; dir: 180 }
        ListElement { lat: 0.5275; lon: 103.2705; dir: 210 }
        ListElement { lat: 0.5280; lon: 103.2715; dir: 240 }
        ListElement { lat: 0.5285; lon: 103.2725; dir: 260 }
        ListElement { lat: 0.5260; lon: 103.2675; dir: 300 }
        ListElement { lat: 0.5265; lon: 103.2688; dir: 320 }
        ListElement { lat: 0.5270; lon: 103.2702; dir: 350 }
        ListElement { lat: 0.5275; lon: 103.2712; dir: 15  }
        ListElement { lat: 0.5280; lon: 103.2722; dir: 40  }
        ListElement { lat: 0.5295; lon: 103.2690; dir: 60  }
        ListElement { lat: 0.5290; lon: 103.2700; dir: 100 }
        ListElement { lat: 0.5285; lon: 103.2710; dir: 140 }
        ListElement { lat: 0.5280; lon: 103.2720; dir: 200 }
        ListElement { lat: 0.5275; lon: 103.2730; dir: 270 }
    }

    Plugin {
        id: mapPlugin
        name: "osm"
        PluginParameter {
            name: "osm.mapping.custom.host"
            value: "http://localhost/osm/"
        }
        PluginParameter {
            name: "osm.mapping.providersrepository.disabled"
            value: true
        }
    }

    Map {
        id: map
        anchors.fill: parent
        plugin: mapPlugin
        center: QtPositioning.coordinate(0.527819883, 103.2707025)
        zoomLevel: 15
        activeMapType: supportedMapTypes[1]

        MapItemView {
            model: currentModel
            delegate: Component {
                MapQuickItem {
                    coordinate: QtPositioning.coordinate(lat, lon)
                    anchorPoint.x: 12
                    anchorPoint.y: 12

                    sourceItem: Item {
                        width: 24
                        height: 24
                        rotation: dir

                        // Arrow body — thin horizontal rectangle
                        Rectangle {
                            x: 3
                            y: 11
                            width: 17
                            height: 2
                            color: "#bd0b0b"
                        }

                        // Arrowhead top leg
                        // 5px diagonal at 45° upward from tip (x=20, y=12)
                        Rectangle {
                            x: 14
                            y: 7
                            width: 9
                            height: 2
                            color: "#bd0b0b"
                            rotation: -38
                            transformOrigin: Item.TopRight
                        }

                        // Arrowhead bottom leg
                        Rectangle {
                            x: 14
                            y: 13
                            width: 9
                            height: 2
                            color: "#bd0b0b"
                            rotation: 38
                            transformOrigin: Item.TopRight
                        }
                    }
                }
            }
        }
    }
}