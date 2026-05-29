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

    // ── Your data array — edit this freely ──────────────────────────
    property var currentArray: [
        {"lat": 0.5270, "lon": 103.2680, "dir": 90 },
        {"lat": 0.5275, "lon": 103.2690, "dir": 90 },
        {"lat": 0.5280, "lon": 103.2700, "dir": 90 },
        {"lat": 0.5285, "lon": 103.2710, "dir": 90 },
        {"lat": 0.5290, "lon": 103.2720, "dir": 90},
        {"lat": 0.5265, "lon": 103.2685, "dir": 90},
        {"lat": 0.5270, "lon": 103.2695, "dir": 90},
        {"lat": 0.5275, "lon": 103.2705, "dir": 90},
        {"lat": 0.5280, "lon": 103.2715, "dir": 90},
        {"lat": 0.5285, "lon": 103.2725, "dir": 90},
        {"lat": 0.5260, "lon": 103.2675, "dir": 90},
        {"lat": 0.5265, "lon": 103.2688, "dir": 90},
        {"lat": 0.5270, "lon": 103.2702, "dir": 90},
        {"lat": 0.5275, "lon": 103.2712, "dir": 90 },
        {"lat": 0.5280, "lon": 103.2722, "dir": 90 },
        {"lat": 0.5295, "lon": 103.2690, "dir": 90 },
        {"lat": 0.5290, "lon": 103.2700, "dir": 90},
        {"lat": 0.5285, "lon": 103.2710, "dir": 90},
        {"lat": 0.5280, "lon": 103.2720, "dir": 90},
        {"lat": 0.5275, "lon": 103.2730, "dir": 90}
    ]

    // ── ListModel populated from the array at startup ────────────────
    ListModel {
        id: currentModel
    }

    Component.onCompleted: {
        for (var i = 0; i < currentArray.length; i++) {
            currentModel.append(currentArray[i])
        }
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
                    anchorPoint.x: 2
                    anchorPoint.y: 12

                    sourceItem: Shape {
                        width: 24
                        height: 24
                        rotation: dir
                        antialiasing: true
                        layer.enabled: true
                        layer.samples: 4

                        ShapePath {
                            strokeColor: "#bd0b0b"
                            strokeWidth: 2
                            fillColor:   "transparent"
                            capStyle:    ShapePath.RoundCap
                            joinStyle:   ShapePath.RoundJoin
                            startX: 2;  startY: 12
                            PathLine { x: 17; y: 12 }
                        }

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