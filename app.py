import requests
from datetime import datetime, timezone
from dateutil import parser



LATITUDE = 52.52
LONGITUDE = 13.41

def get_weather():
    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={LATITUDE}&longitude={LONGITUDE}"
        f"&hourly=temperature_2m,relative_humidity_2m&timezone=UTC"
    )

    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    # UTC-aware current hour
    current_utc = datetime.now(timezone.utc).replace(minute=0, second=0, microsecond=0)
    
    times = [parser.isoparse(t).replace(tzinfo=timezone.utc) for t in data["hourly"]["time"]]

    # Convert all returned times to datetime
    temperatures = data["hourly"]["temperature_2m"]
    humidities = data["hourly"]["relative_humidity_2m"]

    # Find closest timestamp
    closest_index = min(range(len(times)), key=lambda i: abs(times[i] - current_utc))

    return {
        "timestamp": times[closest_index].isoformat(),
        "temperature": temperatures[closest_index],
        "humidity": humidities[closest_index]
    }

if __name__ == "__main__":
    weather = get_weather()
    print("Fetched Weather Data:")
    print(weather)
