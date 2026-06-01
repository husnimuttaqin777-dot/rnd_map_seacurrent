import requests
import numpy as np
import pandas as pd
import os

from datetime import datetime

from concurrent.futures import (
    ThreadPoolExecutor,
    as_completed
)

from shapely.geometry import (
    Point,
    Polygon
)

# ================= ZONE =================

zone_lat = [
    1.155785, 1.155014, 1.156945, 1.151677,
    1.143302, 1.138111, 1.148528, 1.151154
]

zone_lon = [
    103.893489, 103.896592, 103.897982, 103.914801,
    103.920651, 103.917728, 103.909467, 103.895794
]

n_points = 30


def generate_points_in_zone(
    zone_lat,
    zone_lon,
    n_points
):

    polygon = Polygon(
        zip(zone_lon, zone_lat)
    )

    lat_grid = np.linspace(
        min(zone_lat),
        max(zone_lat),
        int(np.ceil(np.sqrt(n_points*3)))
    )

    lon_grid = np.linspace(
        min(zone_lon),
        max(zone_lon),
        int(np.ceil(np.sqrt(n_points*3)))
    )

    inside = []

    for lat in lat_grid:
        for lon in lon_grid:

            if polygon.contains(
                Point(lon, lat)
            ):

                inside.append(
                    (lat, lon)
                )

    if len(inside) > n_points:

        idx = np.round(

            np.linspace(
                0,
                len(inside)-1,
                n_points
            )

        ).astype(int)

        inside = [
            inside[i]
            for i in idx
        ]

    return inside


coords = generate_points_in_zone(
    zone_lat,
    zone_lon,
    n_points
)

filename = "wind_now.csv"

if os.path.exists(filename):
    os.remove(filename)


def fetch(lat, lon):

    url = (

        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}"
        f"&longitude={lon}"
        f"&hourly=wind_speed_10m,"
        f"wind_direction_10m"
        f"&forecast_days=1"
        f"&timezone=Asia/Jakarta"

    )

    try:

        r = requests.get(
            url,
            timeout=10
        )

        data = r.json()

        hourly = data.get(
            "hourly",
            {}
        )

        times = hourly.get(
            "time",
            []
        )

        speed = hourly.get(
            "wind_speed_10m",
            []
        )

        direction = hourly.get(
            "wind_direction_10m",
            []
        )

        if len(times) == 0:
            return None

        now = datetime.now().strftime(
            "%Y-%m-%dT%H:00"
        )

        try:

            idx = times.index(now)

        except:

            idx = 0

        return {

            "latitude": lat,

            "longitude": lon,

            "time": times[idx],

            "wind_speed": speed[idx],

            "wind_direction": direction[idx]

        }

    except Exception as e:

        print(
            f"ERROR {lat:.4f} "
            f"{lon:.4f} "
            f"-- {e}"
        )

        return None


rows = []

with ThreadPoolExecutor(
    max_workers=10
) as executor:

    futures = {

        executor.submit(
            fetch,
            lat,
            lon
        ): (lat, lon)

        for lat, lon in coords
    }

    for i, future in enumerate(

        as_completed(futures),

        1

    ):

        result = future.result()

        if result:

            rows.append(
                result
            )

        print(
            f"{i}/{len(coords)} done"
        )


df = pd.DataFrame(rows)

if not df.empty:

    df.to_csv(
        filename,
        index=False
    )

    print(df.head())

    print(
        "saved:",
        filename
    )

else:

    print(
        "No data collected"
    )