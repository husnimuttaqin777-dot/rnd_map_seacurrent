import requests
import numpy as np
import pandas as pd
from datetime import datetime

import os

filename = "sea_current_now.csv"

if os.path.exists(filename):

    os.remove(filename)

    print("csv lama dihapus")

else:

    print("csv belum ada")

# area grid
lat_top = 0.318253
lon_left = 103.645815

lat_bottom = -0.343617
lon_right = 104.415788

# 10x10 = 100 titik
lat_grid = np.linspace(lat_top, lat_bottom, 10)
lon_grid = np.linspace(lon_left, lon_right, 10)

rows = []

count = 0



for lat in lat_grid:
    for lon in lon_grid:

        count += 1
        print(f"Request {count}/100")

        url = (
            f"https://marine-api.open-meteo.com/v1/marine?"
            f"latitude={lat}"
            f"&longitude={lon}"
            f"&hourly=ocean_current_velocity,ocean_current_direction"
            f"&forecast_days=1"
        )

        try:

            r = requests.get(url, timeout=15)
            data = r.json()

            # ambil data jam pertama / current hour
            speed = data["hourly"]["ocean_current_velocity"][0]
            direction = data["hourly"]["ocean_current_direction"][0]
            time_data = data["hourly"]["time"][0]

            rows.append({
                "latitude": lat,
                "longitude": lon,
                "time": time_data,
                "sea_current_speed": speed,
                "direction": direction
            })

        except Exception as e:
            print("ERROR", lat, lon, e)

df = pd.DataFrame(rows)

filename = "sea_current_now.csv"

df.to_csv(
    filename,
    index=False
)

print("saved:", filename)
print(df.head())