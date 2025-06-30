from fetch import get_weather
from db import insert_weather_data, wait_for_db

if __name__ == "__main__":
    wait_for_db()
    city = "Sendling"  # change as needed
    weather = get_weather(city)
    print("Fetched Weather Data:", weather)
    insert_weather_data(weather)
    print("Inserted data into TimescaleDB.")