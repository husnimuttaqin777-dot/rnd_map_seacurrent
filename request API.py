import requests
import numpy as np
import pandas as pd
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

filename = "sea_current_now.csv"

if os.path.exists(filename):
    os.remove(filename)
    print("csv lama dihapus")
else:
    print("csv belum ada")

# area grid
lat_top    =  1.510931
lon_left   =  103.565077
lat_bottom =  0.7
lon_right  = 104.428989

lat_grid = np.linspace(lat_top, lat_bottom, 15)
lon_grid = np.linspace(lon_left, lon_right, 15)

coords = [(lat, lon) for lat in lat_grid for lon in lon_grid]
total = len(coords)


def fetch(lat, lon):
    url = (
        f"https://marine-api.open-meteo.com/v1/marine?"
        f"latitude={lat}"
        f"&longitude={lon}"
        f"&hourly=ocean_current_velocity,ocean_current_direction"
        f"&forecast_days=1"
    )
    r = requests.get(url, timeout=5)
    data = r.json()
    speed     = data["hourly"]["ocean_current_velocity"][0]
    direction = data["hourly"]["ocean_current_direction"][0]
    time_data = data["hourly"]["time"][0]
    return {
        "latitude": lat,
        "longitude": lon,
        "time": time_data,
        "sea_current_speed": speed,
        "direction": direction
    }


rows = []
done = 0

with ThreadPoolExecutor(max_workers=20) as executor:
    futures = {executor.submit(fetch, lat, lon): (lat, lon) for lat, lon in coords}

    for future in as_completed(futures):
        lat, lon = futures[future]
        done += 1
        try:
            rows.append(future.result())
            print(f"Request {done}/{total} OK")
        except Exception as e:
            print(f"ERROR {lat:.4f} {lon:.4f} — {e}")

df = pd.DataFrame(rows)
df.to_csv(filename, index=False)

print("saved:", filename)
print(df.head())