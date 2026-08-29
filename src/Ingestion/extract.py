import json
import os
import requests

from datetime import datetime, timedelta

from dotenv import load_dotenv

from src.common.logger import get_logger

load_dotenv()

ADZUNA_APP_ID = os.getenv("ADZUNA_APP_ID")
ADZUNA_APP_KEY = os.getenv("ADZUNA_APP_KEY")

logger = get_logger(__name__, "extraction.log")


def api_extraction():

    today_date = datetime.now()

    date_10_days_ago = today_date - timedelta(days=15)

    start_date = date_10_days_ago.strftime('%Y-%m-%d')
    end_date = today_date.strftime("%Y-%m-%d")

    # ---------------------------------------------------
    # GEOCODING MAPPING API
    # ---------------------------------------------------
    geocoding_url = (
        "https://psgc.cloud/api/cities"
    )

    # ---------------------------------------------------
    # JOB ADZUNA API
    # ---------------------------------------------------
    adzuna_url = (
        "https://api.adzuna.com/v1/api/jobs/gb/search/1"
    )

    adzuna_params = {
        "app_id": ADZUNA_APP_ID,
        "app_key": ADZUNA_APP_KEY,
        "results_per_page": 50,
        "content-type": "application/json",
    }

    # ---------------------------------------------------
    # JOB ARBEITNOW API
    # ---------------------------------------------------
    arbeitnow_url = (
        "https://www.arbeitnow.com/api/job-board-api"
    )

    # ---------------------------------------------------
    # JOB REMOTIVE API
    # ---------------------------------------------------
    remotive_url = (
        "https://remotive.com/api/remote-jobs"
    )

    remotive_params = {
       "category": "software-dev",
       "company_name": "remotive",
       "search": "front end"
    }


    logger.info(
        f"Extracting weather data: {start_date} → {end_date}"
    )


    try:

        # GEOCODING MAPPING REQUEST
        logger.info("Starting Geocoding API Request...")

        geocoding_response =  requests.get(geocoding_url, timeout=20)

        geocoding_response.raise_for_status()

        geocoding = geocoding_response.json()

        logger.info(
            f" Weather Request Successful: {geocoding_response.status_code}"
        )


        # JOB ADZUNA REQUEST
        logger.info("Starting Adzuna API Request...")

        adzuna_response =  requests.get(
            adzuna_url, 
            params=adzuna_params, 
            timeout=20
            )

        adzuna_response.raise_for_status()

        adzuna = adzuna_response.json()

        logger.info(
            f"Adzuna API successful: "
            f"{adzuna_response.status_code}"
        )


        # JOB ARBEITNOW REQUEST
        logger.info("Starting Arbeitnow API Request...")

        arbeitnow_response =  requests.get(
            arbeitnow_url, 
            timeout=20
            )

        arbeitnow_response.raise_for_status()

        arbeitnow = arbeitnow_response.json()

        logger.info(
            f"Arbeitnow Request Successful: {arbeitnow_response.status_code}"
        )

        # JOB REMOTIVE REQUEST
        logger.info("Starting Remotive API Request...")

        remotive_response = requests.get(
            remotive_url, 
            params=remotive_params, 
            timeout=20
            )

        remotive_response.raise_for_status()

        remotive = remotive_response.json()

        logger.info(f"Remotive Request Successful: {remotive_response.status_code}")


        return {
            "geocoding": geocoding,
            "adzuna": adzuna,
            "arbeitnow": arbeitnow,
            "remotive": remotive
        }



    except requests.exceptions.Timeout:
        logger.error(
            "API request timed out."
            )
        raise

    except requests.exceptions.ConnectionError:
        logger.error(
            "API connection error."
            )
        raise

    except requests.exceptions.HTTPError as e:
        logger.error(
            f"HTTP error "
            f"{e.response.status_code}: "
            f"{e.response.text}"
        )
        raise

    except json.JSONDecodeError:
        logger.error(
            "Invalid JSON response."
            )
        raise

    except Exception:
        logger.info(
            "Unexpected error during API extration."
            )


