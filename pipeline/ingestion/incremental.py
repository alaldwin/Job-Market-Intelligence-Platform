from datetime import datetime, timedelta

from pipeline.ingestion.state_manager import get_last_date


def get_incremental_dates(source):

    today = datetime.now().date()

    last_date = get_last_date(source)

    if last_date is None:
        # First ingestion
        start_date = today - timedelta(days=15)

    else:
        # Incremental ingestion
        last_date = datetime.strptime(
            last_date,
            "%Y-%m-%d"
        ).date()

        start_date = last_date + timedelta(days=1)

    if start_date > today:
        return None, None

    return (
        start_date.strftime("%Y-%m-%d"),
        today.strftime("%Y-%m-%d")
    )