import json
import os

from src.common.logger import get_logger

logger = get_logger(__name__, "save_json.log")


RAW_DIR = "data/raw"


def save_json(data, source, batch_date):

    source_dir = os.path.join(
        RAW_DIR,
        source
    )

    os.makedirs(
        source_dir,
        exist_ok=True
    )

    file_path = os.path.join(
        source_dir,
        f"{batch_date}.json"
    )

    with open(
        file_path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False
        )

    logger.info(
        f"JSON successfully saved: {file_path}"
    )