import psycopg2
import os
import time

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

def wait_for_db(max_retries=10, delay=3):
    retries = 0
    while retries < max_retries:
        try:
            conn = psycopg2.connect(
                host=os.getenv("DB_HOST", "localhost"),
                port=os.getenv("DB_PORT", "5432"),
                dbname=os.getenv("DB_NAME", "weather"),
                user=os.getenv("DB_USER", "postgres"),
                password=os.getenv("DB_PASSWORD", "postgres"),
            )
            conn.close()
            print("Database is ready!")
            return
        except psycopg2.OperationalError:
            retries += 1
            print(f"Database not ready, retrying ({retries}/{max_retries})...")
            time.sleep(delay)
    raise Exception("Database not ready after multiple retries.")
