
from src.common.logger import get_logger
from src.Ingestion.extract import api_extraction

logger = get_logger(__name__, "Main.log")

def main():

    data = api_extraction()




if __name__ == "__main__":
    main()
