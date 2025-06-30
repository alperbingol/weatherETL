import requests
from datetime import datetime, timezone, timedelta
from dateutil import parser
from zoneinfo import ZoneInfo
import psycopg2
import os


def get_coordinates(city_name):
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}"
    response = requests.get(url)
    response.raise_for_status()
    results = response.json().get("results")
    
    if not results:
        raise Exception(f"City '{city_name}' not found.")
    
    city = results[0]
    return {
        "latitude": city["latitude"],
        "longitude": city["longitude"],
        "timezone": city["timezone"],
        "name": city["name"]
    }

def get_weather(city_name):

    location = get_coordinates(city_name)
    LATITUDE, LONGITUDE, TIMEZONE = location["latitude"], location["longitude"], location["timezone"]

    print(f"For {location["name"]},\n the latitude: {LATITUDE}, \n the longitude: {LONGITUDE},\n the timezone: {TIMEZONE}")

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
    current_local = datetime.now(ZoneInfo(api_timezone))
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
        "city": location["name"],
        "temperature": temperatures[closest_index],
        "humidity": humidities[closest_index]
    }

def insert_weather_data(weather):
    """Insert a weather record into TimescaleDB"""
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.getenv("DB_NAME", "weather"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "postgres"),
    )
    cur = conn.cursor()
    insert_sql = """
        INSERT INTO weather_data (timestamp, city, temperature, humidity)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (timestamp, city) DO NOTHING;
    """
    cur.execute(insert_sql, (
        weather["timestamp"],
        weather["city"],
        weather["temperature"],
        weather["humidity"],
    ))
    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    
    city_name = "81373"

    weather = get_weather(city_name)
    print(f"Fetched Weather Data: {weather}")
    insert_weather_data(weather)
    print("Inserted data into TimescaleDB.")
