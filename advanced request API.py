import asyncio
import aiohttp
import numpy as np
import pandas as pd
import os
from datetime import datetime

# ── Config ───────────────────────────────────────────────────────────────
FILENAME    = "sea_current_indonesia.csv"
MAX_WORKERS = 20
TIMEOUT_SEC = 20
MAX_RETRIES = 3
RETRY_DELAY = 2.0

# ── Sub-regions of Indonesia ─────────────────────────────────────────────
# Each region gets its own 20x20 grid = 400 points per region
# Overlap slightly at borders so no gaps between regions
REGIONS = [
    {"name": "Selat Malaka & Sumatra Barat",  "lat_top":  6.0,  "lat_bot":  -6.0, "lon_left":  94.0, "lon_right": 106.0},
    {"name": "Jawa & Selat Sunda",             "lat_top":  3.0,  "lat_bot":  -9.5, "lon_left": 104.0, "lon_right": 112.0},
    {"name": "Bali & Nusa Tenggara",           "lat_top":  2.0,  "lat_bot": -10.5, "lon_left": 111.0, "lon_right": 120.0},
    {"name": "Kalimantan & Laut Jawa",         "lat_top":  7.0,  "lat_bot":  -5.0, "lon_left": 107.0, "lon_right": 118.0},
    {"name": "Sulawesi & Laut Banda",          "lat_top":  5.0,  "lat_bot":  -8.0, "lon_left": 118.0, "lon_right": 128.0},
    {"name": "Maluku & Laut Seram",            "lat_top":  4.0,  "lat_bot":  -8.0, "lon_left": 126.0, "lon_right": 136.0},
    {"name": "Papua Barat & Teluk Cendrawasih","lat_top":  2.0,  "lat_bot":  -8.0, "lon_left": 130.0, "lon_right": 141.0},
]

GRID_SIZE = 20   # per region — tune up/down as needed

# ── Build all points ──────────────────────────────────────────────────────
all_points = []
for region in REGIONS:
    lats = np.linspace(region["lat_top"], region["lat_bot"], GRID_SIZE)
    lons = np.linspace(region["lon_left"], region["lon_right"], GRID_SIZE)
    for lat in lats:
        for lon in lons:
            all_points.append({"region": region["name"], "lat": lat, "lon": lon})

print(f"Total points across {len(REGIONS)} regions: {len(all_points)}")

# ── Single async fetch ────────────────────────────────────────────────────
async def fetch_point(session, semaphore, idx, total, pt):
    url = (
        f"https://marine-api.open-meteo.com/v1/marine"
        f"?latitude={pt['lat']}&longitude={pt['lon']}"
        f"&hourly=ocean_current_velocity,ocean_current_direction"
        f"&forecast_days=1"
    )
    async with semaphore:
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                async with session.get(url, timeout=aiohttp.ClientTimeout(total=TIMEOUT_SEC)) as r:
                    if r.status == 429:
                        wait = RETRY_DELAY * attempt
                        print(f"  ⏳ [{idx:>5}/{total}] Rate limited, retry {attempt}/{MAX_RETRIES} in {wait}s...")
                        await asyncio.sleep(wait)
                        continue

                    data = await r.json()

                    if "error" in data or "hourly" not in data:
                        return None   # land point — silent skip

                    speed = data["hourly"]["ocean_current_velocity"][0]
                    direc = data["hourly"]["ocean_current_direction"][0]
                    time_ = data["hourly"]["time"][0]

                    if speed is None or direc is None:
                        return None   # land mask — silent skip

                    print(f"  ✓ [{idx:>5}/{total}] ({pt['lat']:.3f}, {pt['lon']:.3f})  {speed:.2f} m/s  {direc:.0f}°  [{pt['region']}]")
                    return {
                        "region"            : pt["region"],
                        "latitude"          : round(pt["lat"], 6),
                        "longitude"         : round(pt["lon"], 6),
                        "time"              : time_,
                        "sea_current_speed" : speed,
                        "direction"         : direc,
                    }

            except asyncio.TimeoutError:
                await asyncio.sleep(RETRY_DELAY * attempt)
            except Exception as e:
                print(f"  ✗ [{idx:>5}/{total}] ({pt['lat']:.3f}, {pt['lon']:.3f})  ERROR: {e}")
                return None

        return None

# ── Process region by region ──────────────────────────────────────────────
async def main():
    if os.path.exists(FILENAME):
        os.remove(FILENAME)

    total     = len(all_points)
    semaphore = asyncio.Semaphore(MAX_WORKERS)
    t_start   = datetime.now()
    all_rows  = []

    print(f"\nFetching {total} points across {len(REGIONS)} regions...\n")

    async with aiohttp.ClientSession() as session:
        for region in REGIONS:
            region_pts = [p for p in all_points if p["region"] == region["name"]]
            base_idx   = all_points.index(region_pts[0])

            print(f"\n{'─'*55}")
            print(f"  Region: {region['name']}  ({len(region_pts)} points)")
            print(f"{'─'*55}")

            tasks = [
                fetch_point(session, semaphore, base_idx + i + 1, total, pt)
                for i, pt in enumerate(region_pts)
            ]
            results = await asyncio.gather(*tasks)
            rows    = [r for r in results if r is not None]
            all_rows.extend(rows)

            print(f"  → {len(rows)}/{len(region_pts)} sea points collected")
            await asyncio.sleep(1.0)   # pause between regions

    elapsed = (datetime.now() - t_start).total_seconds()
    df      = pd.DataFrame(all_rows)

    # remove duplicate points where regions overlap
    df = df.drop_duplicates(subset=["latitude", "longitude"])
    df.to_csv(FILENAME, index=False)

    print(f"\n{'═'*55}")
    print(f"  Done in     : {elapsed:.1f}s")
    print(f"  Saved       : {FILENAME}")
    print(f"  Total rows  : {len(df)}")
    print(f"  Regions     : {len(REGIONS)}")
    print(f"{'═'*55}\n")

    # summary per region
    print(df.groupby("region")["sea_current_speed"].agg(["count","mean","max"]).round(3).to_string())

if __name__ == "__main__":
    asyncio.run(main())