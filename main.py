# Pipeline
from src.ingestion.extract import api_extraction

from src.common.logger import get_logger

logger = get_logger(__name__, "main.log")

def main():

    try:

        logger.info("Pipeline Started...")

        # extraction
        data = api_extraction()
        print(data)

        if data is None:
            logger.info("Pipeline finished: no new data.")
            return

    except Exception as e:
        logger.info(f"{e}.")

    logger.info("Extraction completed successfully.")

    

    
if __name__ == "__main__":
    main()
