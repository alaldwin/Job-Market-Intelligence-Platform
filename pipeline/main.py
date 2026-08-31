# Pipeline
from src.ingestion.extract import api_extraction

from src.common.logger import get_logger
from src.validation.validation_manager import validate_data

logger = get_logger(__name__, "main.log")

def main():

    logger.info("Pipeline Started")

    try:

        # extraction
        logger.info("Starting Extraction...")

        data = api_extraction()

        if data is None:
            logger.info("Pipeline finished: no new data.")

            return

        logger.info("Extraction is Successfully.")


        # Validation
        logger.info(
        "Starting Validation..."
    )

        for source, source_data in data.items():
            

            validate_data(source, source_data)

            logger.info(f"{source} validation PASSED.")

        logger.info(
            "All validation completed."
        )

    except Exception as e:
        logger.info(f"{e}.")

    logger.info("Pipeline completed successfully.")

    

    
if __name__ == "__main__":
    main()
