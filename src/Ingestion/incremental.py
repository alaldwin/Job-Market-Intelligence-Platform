from datetime import datetime, timedelta

from src.ingestion.state_manager import get_last_date


def get_incremental_dates(source):

    today = datetime.now().date()

    last_date = get_last_date(source)

    # First ingestion
    if last_date is None:

        start_date = today - timedelta(days=15)

    # Incremental ingestion
    else:

        last_ingestion_date = datetime.strptime(
            last_date,
            "%Y-%m-%d"
        ).date()

        start_date = last_ingestion_date + timedelta(days=1)

    # Nothing new
    if start_date > today:

        return None, None

    return (
        start_date.strftime("%Y-%m-%d"),
        today.strftime("%Y-%m-%d")
    )