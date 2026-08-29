# Pipeline
from src.ingestion.extract import api_extraction

from src.common.logger import get_logger

logger = get_logger(__name__, "main.log")

def main():

    logger.info("Pipeline Started...")

    # extraction
    data = api_extraction()
    print(data)


    
if __name__ == "__main__":
    main()
