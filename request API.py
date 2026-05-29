import asyncio
import aiohttp
import numpy as np
import pandas as pd
import os
from datetime import datetime

# ── Config ──────────────────────────────────────────────────────────────
FILENAME     = "sea_current_now.csv"
LAT_TOP      =   5.719486
LON_LEFT     =  94.827627
LAT_BOTTOM   =  -8.879424
LON_RIGHT    = 140.225176
GRID_SIZE    = 20          # 20×20 = 400 points
MAX_WORKERS  = 20          # concurrent requests (safe limit)
TIMEOUT_SEC  = 50

# ── Grid ─────────────────────────────────────────────────────────────────
lat_grid = np.linspace(LAT_TOP, LAT_BOTTOM, GRID_SIZE)
lon_grid = np.linspace(LON_LEFT, LON_RIGHT, GRID_SIZE)
points   = [(lat, lon) for lat in lat_grid for lon in lon_grid]

# ── Single async fetch ────────────────────────────────────────────────────
async def fetch_point(session, semaphore, idx, total, lat, lon):
    url = (
        f"https://marine-api.open-meteo.com/v1/marine"
        f"?latitude={lat}&longitude={lon}"
        f"&hourly=ocean_current_velocity,ocean_current_direction"
        f"&forecast_days=1"
    )
    async with semaphore:
        try:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=TIMEOUT_SEC)) as r:
                data  = await r.json()
                speed = data["hourly"]["ocean_current_velocity"][0]
                direc = data["hourly"]["ocean_current_direction"][0]
                time_ = data["hourly"]["time"][0]
                print(f"  ✓ [{idx:>3}/{total}] ({lat:.4f}, {lon:.4f})  {speed:.2f} m/s  {direc:.0f}°")
                return {
                    "latitude"          : round(lat, 6),
                    "longitude"         : round(lon, 6),
                    "time"              : time_,
                    "sea_current_speed" : speed,
                    "direction"         : direc,
                }
        except Exception as e:
            print(f"  ✗ [{idx:>3}/{total}] ({lat:.4f}, {lon:.4f})  ERROR: {e}")
            return None

# ── Main coroutine ────────────────────────────────────────────────────────
async def main():
    if os.path.exists(FILENAME):
        os.remove(FILENAME)
        print(f"Deleted old file: {FILENAME}")

    total     = len(points)
    semaphore = asyncio.Semaphore(MAX_WORKERS)
    t_start   = datetime.now()

    print(f"\nFetching {total} grid points ({GRID_SIZE}×{GRID_SIZE}) with {MAX_WORKERS} concurrent workers...\n")

    async with aiohttp.ClientSession() as session:
        tasks = [
            fetch_point(session, semaphore, idx + 1, total, lat, lon)
            for idx, (lat, lon) in enumerate(points)
        ]
        results = await asyncio.gather(*tasks)

    elapsed = (datetime.now() - t_start).total_seconds()

    rows = [r for r in results if r is not None]
    df   = pd.DataFrame(rows)
    df.to_csv(FILENAME, index=False)

    print(f"\n{'─'*50}")
    print(f"  Done in     : {elapsed:.1f}s  (was ~{total * 1.5 / 60:.0f} min sequential)")
    print(f"  Saved       : {FILENAME}")
    print(f"  Points OK   : {len(rows)}/{total}")
    print(f"  Failed      : {total - len(rows)}")
    print(f"{'─'*50}\n")
    print(df.head(10).to_string(index=False))

# ── Entry point ───────────────────────────────────────────────────────────
if __name__ == "__main__":
    asyncio.run(main())