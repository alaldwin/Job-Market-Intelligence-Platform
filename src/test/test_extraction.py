import pytest
import requests

from unittest.mock import patch, Mock
from src.Ingestion.extract import api_extraction

@patch("src.Ingestion.extract.requests.get")
def test_api_extraction_success(mock_get):

    mock_response = Mock()

    mock_response.status_code = 200

    mock_response.json.return_value = {
        "test": "data"
    }

    mock_response.raise_for_status.return_value = None

    mock_get.return_value = mock_response

    data = api_extraction()

    assert isinstance(data, dict)
    assert "weather" in data
    assert "geocoding" in data
    assert "adzuna" in data
    assert "arbeitnow" in data
    assert "remotive" in data