import requests
from datetime import datetime, timezone, timedelta
from dateutil import parser
from zoneinfo import ZoneInfo



print("datetime.now():", datetime.now())
print("datetime.now(timezone.utc):", datetime.now(timezone.utc))


LATITUDE = 52.52
LONGITUDE = 13.41

def get_weather():
    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={LATITUDE}&longitude={LONGITUDE}"
        f"&hourly=temperature_2m,relative_humidity_2m&timezone=auto"
    )

    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    # Use the timezone returned by the API
    api_timezone = data["timezone"]
    current_local = datetime.now(ZoneInfo(api_timezone)).replace(minute=0, second=0, microsecond=0)
    print(f"Current time in {api_timezone}: {current_local}")


    # API already returns local time due to timezone=auto
    #times = [parser.isoparse(t) for t in data["hourly"]["time"]]
    times = [parser.isoparse(t).replace(tzinfo=ZoneInfo(api_timezone)) for t in data["hourly"]["time"]]


    # Find closest time
    closest_index = min(range(len(times)), key=lambda i: abs(times[i] - current_local))

    # Convert all returned times to datetime
    temperatures = data["hourly"]["temperature_2m"]
    humidities = data["hourly"]["relative_humidity_2m"]

    return {
        "timestamp": times[closest_index].isoformat(),
        "temperature": temperatures[closest_index],
        "humidity": humidities[closest_index]
    }

if __name__ == "__main__":
    weather = get_weather()
    print("Fetched Weather Data:")
    print(weather)
