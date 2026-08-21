import json
import os
import requests
from datetime import datetime, timedelta

from src.common.logger import get_logger

logger = get_logger(__name__, "Extraction.log")

raw_dir = "data/raw"
json_file = os.path.join(raw_dir, "weather.josn")

os.makedirs(raw_dir, exist_ok=True)


def api_extraction():

    today_date = datetime.now()

    date_10_days_ago = today_date - timedelta(days=15)

    start_date = date_10_days_ago.strftime('%Y-%m-%d')
    end_date = today_date.strftime("%Y-%m-%d")

    url = (
        "https://api.open-meteo.com/v1/forecast?"
        "latitude=14.6042"
        "&longitude=120.9822"
        "&daily=sunset,sunrise,weather_code"
        "&hourly="
        "temperature_2m,"
        "relative_humidity_2m,"
        "wind_speed_10m,"
        "precipitation_probability,"
        "weather_code,"
        "surface_pressure"
        "&current="
        "surface_pressure,"
        "weather_code,"
        "precipitation,"
        "temperature_2m,"
        "relative_humidity_2m,"
        "wind_speed_10m"
        f"&start_date={start_date}"
        f"&end_date={end_date}"
    )

    logger.info(
        f"Extracting weather data: {start_date} → {end_date}"
    )

    try:

        response = requests.get(url, timeout=30)

        response.raise_for_status()

        data = response.json()

        logger.info(
            f"API request successful: {response.status_code}"
        )

        return data

    except requests.exceptions.Timeout:
        print(f"Request time out for {url}")
        raise
    except requests.exceptions.ConnectionError:
        print(f"Connection error for {url}")
        raise
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error {e.response.status_code}: {e.response.text}")
        raise
    except json.JSONDecodeError:
        print(f"Invalid JSON response from {url}")
        print(f"Response text: {response.text}")
        raise


