import logging
from pathlib import Path as path

root = path(__file__).resolve().parents[2]

log_dir = root / "logs"
log_dir.mkdir(parents=True, exist_ok=True)

log_format = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

def get_logger(name: str, filename: str) -> logging.Logger:

    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    file_handler = logging.FileHandler(
        log_dir / filename, 
        encoding="utf-8"
        )
    
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    logger.propagate = False

    return logger