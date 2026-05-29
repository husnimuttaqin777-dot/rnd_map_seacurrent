import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Shapes 1.15
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

                    // Anchor to the tail of the arrow (left center)
                    // so the arrow grows rightward then rotates from its tail
                    anchorPoint.x: 2
                    anchorPoint.y: 12

                    sourceItem: Shape {
                        width: 24
                        height: 24
                        rotation: dir
                        antialiasing: true
                        layer.enabled: true
                        layer.samples: 4   // MSAA — smooth diagonal lines

                        // Arrow body: tail (2,12) → shaft end (17,12)
                        ShapePath {
                            strokeColor: "#bd0b0b"
                            strokeWidth: 2
                            fillColor:   "transparent"
                            capStyle:    ShapePath.RoundCap
                            joinStyle:   ShapePath.RoundJoin

                            startX: 2;  startY: 12
                            PathLine { x: 17; y: 12 }
                        }

                        // Arrowhead: tip at (22,12), top leg to (15,7)
                        ShapePath {
                            strokeColor: "#bd0b0b"
                            strokeWidth: 2
                            fillColor:   "transparent"
                            capStyle:    ShapePath.RoundCap
                            joinStyle:   ShapePath.RoundJoin

                            startX: 22; startY: 12
                            PathLine { x: 15; y: 7  }
                            PathMove  { x: 22; y: 12 }
                            PathLine  { x: 15; y: 17 }
                        }
                    }
                }
            }
        }
    }
}