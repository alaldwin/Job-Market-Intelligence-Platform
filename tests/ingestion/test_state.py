import json

from src.ingestion.state_manager import (
    save_state,
    get_last_date
)


def test_save_and_get_state(tmp_path, monkeypatch):

    state_file = tmp_path / "state.json"

    monkeypatch.setattr(
        "src.ingestion.state_manager.STATE_FILE",
        str(state_file)
    )

    save_state({
        "adzuna": "2026-08-29"
    })

    result = get_last_date("adzuna")

    assert result == "2026-08-29"