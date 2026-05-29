import requests
from datetime import datetime

LAT = 0.527683
LON = 103.273464

COMPASS = ["N","NNE","NE","ENE","E","ESE","SE","SSE","S","SSW","SW","WSW","W","WNW","NW","NNW"]

def deg_to_compass(deg):
    return COMPASS[round(deg / 22.5) % 16]

def beaufort(v):
    thresholds = [(0.3,0),(1.6,1),(3.4,2),(5.5,3),(8.0,4),(10.8,5),(13.9,6)]
    for limit, bf in thresholds:
        if v < limit:
            return bf
    return 7

def current_level(v):
    if v < 0.5:   return "Low     "
    if v < 1.0:   return "Moderate"
    return "Strong  "

def fetch_currents():
    url = (
        f"https://marine-api.open-meteo.com/v1/marine"
        f"?latitude={LAT}&longitude={LON}"
        f"&hourly=ocean_current_velocity,ocean_current_direction"
        f"&forecast_days=7"
    )
    r = requests.get(url, timeout=10)
    r.raise_for_status()
    return r.json()

def group_by_day(data):
    times     = data["hourly"]["time"]
    velocity  = data["hourly"]["ocean_current_velocity"]
    direction = data["hourly"]["ocean_current_direction"]

    days = {}
    for t, v, d in zip(times, velocity, direction):
        date, hour = t.split("T")
        days.setdefault(date, []).append({"hour": hour, "vel": v, "dir": d})
    return days

def print_day(date, rows):
    dt = datetime.strptime(date, "%Y-%m-%d")
    label = dt.strftime("%A, %d %B %Y")

    print(f"\n{'═' * 70}")
    print(f"  {label}")
    print(f"{'═' * 70}")
    print(f"  {'Time':<8} {'Speed':>8} {'Bft':>4} {'Dir':>7} {'Compass':<7} {'Level':<10}")
    print(f"  {'-'*8} {'-'*8} {'-'*4} {'-'*7} {'-'*7} {'-'*10}")

    vels = [r["vel"] for r in rows if r["vel"] is not None]
    for r in rows:
        if r["vel"] is None or r["dir"] is None:
            continue
        compass = deg_to_compass(r["dir"])
        bf      = beaufort(r["vel"])
        bar     = "█" * int(r["vel"] * 10)
        print(
            f"  {r['hour']:<8}"
            f" {r['vel']:>7.2f}m/s"
            f" {bf:>4}"
            f" {int(r['dir']):>6}°"
            f"  {compass:<7}"
            f" {current_level(r['vel']):<10}"
            f" {bar}"
        )

    if vels:
        avg = sum(vels) / len(vels)
        print(f"\n  Summary → Avg: {avg:.2f} m/s  |  Max: {max(vels):.2f} m/s  |  Min: {min(vels):.2f} m/s")

def main():
    print("Fetching Batam ocean current data…")
    data = fetch_currents()
    days = group_by_day(data)

    for date in sorted(days):
        print_day(date, days[date])

    print(f"\n{'═' * 70}")
    print("  Source: Open-Meteo Marine API · open-meteo.com")
    print(f"{'═' * 70}\n")

if __name__ == "__main__":
    main()