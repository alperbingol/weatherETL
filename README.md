# 🌦️ Weather ETL Pipeline with TimescaleDB

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.12-blue)](https://www.python.org/downloads/release/python-3120/)
[![Docker](https://img.shields.io/badge/Docker-Compose-blue)](https://docs.docker.com/compose/)


This project implements a fully deployable ETL pipeline that:
- Fetches live weather data for any city using the Open-Meteo API
- Inserts weather data into a TimescaleDB database
- Runs everything locally with Docker Compose
- Organizes code into modular, maintainable files

---

## 📂 Project structure

weatheretl/
├─ fetch.py # Fetch coordinates & weather data from API
├─ db.py # Insert data into TimescaleDB; DB readiness check
├─ main.py # Orchestrates the ETL pipeline
├─ requirements.txt # Python dependencies
├─ Dockerfile # Python app image build instructions
├─ docker-compose.yml # Define Python app + TimescaleDB services

---

## 🚀 How it works

1. **Fetch**  
   - Uses the Open-Meteo Geocoding API to get latitude, longitude, and timezone of a city.
   - Queries the Open-Meteo Weather API to get current weather data.
   
2. **Transform**
   - Parses weather data, standardizes timestamps in UTC.

3. **Load**
   - Inserts weather data into a TimescaleDB hypertable.
   - `wait_for_db()` ensures the database is ready before inserting.

---

## 🐳 Running locally

Build and start everything with Docker Compose:
```bash
docker-compose up --build
