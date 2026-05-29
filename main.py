from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtCore import QUrl, QVariant
from PyQt5.QtPositioning import QGeoCoordinate
import csv
from collections import defaultdict

def load_polygons():
    component_polygons = defaultdict(lambda: {"points": [], "type": "", "value": ""})
    polygons = []

    with open("isobath_batam.csv", newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            cid = int(row["ComponentId"])
            try:
                lat = float(row["Latitude"])
                lon = float(row["Longitude"])
                val = float(row["Value1"]) if row["Value1"] else 0.0
            except ValueError:
                continue
            component_polygons[cid]["points"].append(QGeoCoordinate(lat, lon))
            component_polygons[cid]["type"] = row["Type"]
            component_polygons[cid]["value"] = val

    for comp in component_polygons.values():
        coords = comp["points"]
        if len(coords) < 3:
            continue

        center_lat = sum(c.latitude() for c in coords) / len(coords)
        center_lon = sum(c.longitude() for c in coords) / len(coords)
        polygons.append({
            "points": coords,
            "type": comp["type"],
            "value": f"{comp['value']:.1f}",
            "center": QGeoCoordinate(center_lat, center_lon)
        })

    return polygons

app = QGuiApplication([])
engine = QQmlApplicationEngine()

polygons = load_polygons()

print("Isi polygons:", polygons)
print("Tipe polygons:", type(polygons))

engine.rootContext().setContextProperty("allPolygons", polygons)

engine.load(QUrl("main.qml"))
app.exec_()
