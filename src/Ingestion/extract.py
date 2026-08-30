import json
import os
import requests

from dotenv import load_dotenv

from src.common.logger import get_logger

from src.ingestion.incremental import get_incremental_dates
from src.ingestion.state_manager import update_last_date
from src.ingestion.save_json import save_json



load_dotenv()

logger = get_logger(
    __name__, 
    "extraction.log"
    )


ADZUNA_APP_ID = os.getenv("ADZUNA_APP_ID")
ADZUNA_APP_KEY = os.getenv("ADZUNA_APP_KEY")


def api_extraction():

    start_date, end_date = get_incremental_dates(
        "adzuna"
    )

    if start_date is None:

        logger.info(
            "No new data to ingest."
        )

        return None

    logger.info(
        f"Incremental ingestion: "
        f"{start_date} → {end_date}"
    )

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



    # REQUESTS
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




        data = {
            "geocoding": geocoding,
            "adzuna": adzuna,
            "arbeitnow": arbeitnow,
            "remotive": remotive
        }


        save_json(
            geocoding,
            "geocoding",
            end_date
        )

        save_json(
            adzuna,
            "adzuna",
            end_date
        )

        save_json(
            arbeitnow,
            "arbeitnow",
            end_date
        )

        save_json(
            remotive,
            "remotive",
            end_date
        )

        # update State
        update_last_date(
            "adzuna",
            end_date
        )

        return data



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


