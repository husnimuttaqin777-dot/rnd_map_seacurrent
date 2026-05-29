import requests

# Batam
lat = 0.519338
lon = 103.279767

url = (
    f"https://marine-api.open-meteo.com/v1/marine?"
    f"latitude={lat}"
    f"&longitude={lon}"
    f"&hourly=ocean_current_velocity,ocean_current_direction"
    f"&forecast_days=7"
)

r = requests.get(url)
data = r.json()

times = data["hourly"]["time"]
velocity = data["hourly"]["ocean_current_velocity"]
direction = data["hourly"]["ocean_current_direction"]

hari_sekarang = ""

for i in range(len(times)):

    tanggal, jam = times[i].split("T")

    if tanggal != hari_sekarang:
        hari_sekarang = tanggal
        print("\n======================")
        print("Tanggal :", tanggal)
        print("======================")
        print("Jam    Speed(m/s)    Direction")

    print(
        f"{jam}    "
        f"{velocity[i]:4.1f}         "
        f"{direction[i]:3d}°"
    )