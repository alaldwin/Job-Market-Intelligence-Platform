from datetime import datetime, timedelta

from src.ingestion.incremental import get_incremental_dates


def test_first_ingestion(monkeypatch):

    monkeypatch.setattr(
        "src.ingestion.incremental.get_last_date",
        lambda source: None
    )

    start_date, end_date = get_incremental_dates("adzuna")

    today = datetime.now().date()

    expected_start = today.replace(
        day=today.day
    )

    # First ingestion should start 15 days ago
    assert start_date == (
        today.fromordinal(
            today.toordinal() - 15
        ).strftime("%Y-%m-%d")
    )

    assert end_date == today.strftime("%Y-%m-%d")


def test_incremental_ingestion(monkeypatch):

    monkeypatch.setattr(
        "src.ingestion.incremental.get_last_date",
        lambda source: "2026-08-29"
    )

    start_date, end_date = get_incremental_dates("adzuna")

    assert start_date == "2026-08-30"