import pytest
import requests

from unittest.mock import Mock, patch
from src.ingestion.extract import api_extraction

class TestExtraction:

    # Test successful extraction
    @patch("src.ingestion.extract.requests.get")
    def test_api_extraction_success(self, mock_get):

        """
            @patch → replaces requests.get() with a fake
            Mock()  → creates a fake API response
            200     → simulates successful request
            json()  → provides fake API data
            api_extraction() → runs your function
            assert  → checks the result

            api_extraction() returns a dictionary

            If the APIs respond successfully, 
            does my extraction function return the expected data structure?
        """

        mock_response = Mock()

        mock_response.status_code = 200

        mock_response.json.return_value = {
            "test": "data"
        }

        mock_response.raise_for_status.return_value = None

        mock_get.return_value = mock_response

        data = api_extraction()

        assert isinstance(data, dict)

        assert "geocoding" in data
        assert "adzuna" in data
        assert "arbeitnow" in data
        assert "remotive" in data



    # Test that all APIs were actually called
    @patch("src.ingestion.extract.requests.get")
    def test_all_apis_called(self, mock_get):

        mock_response = Mock()

        mock_response.status_code = 200

        mock_response.raise_for_status.return_value = None

        mock_response.json.return_value = {}

        mock_get.return_value = mock_response

        api_extraction()

        assert mock_get.call_count == 4



    # Test HTTP errors
    @patch("src.ingestion.extract.requests.get")
    def test_api_extraction_http_error(self, mock_get):

        mock_response = Mock()

        mock_response.status_code = 400

        mock_response.text = "Bad Request"

        error = requests.exceptions.HTTPError("400 Bad Request")

        error.response = mock_response

        mock_response.raise_for_status.side_effect = error

        mock_get.return_value = mock_response

        with pytest.raises(requests.exceptions.HTTPError):
            api_extraction()



    # Test timeout
    @patch("src.ingestion.extract.requests.get")
    def test_api_extraction_timeout(self, mock_get):

        mock_get.side_effect = requests.exceptions.Timeout()

        with pytest.raises(requests.exceptions.Timeout):

            api_extraction()



    # Test connection error
    @patch("src.ingestion.extract.requests.get")
    def test_api_extraction_connection_error(self, mock_get):

        mock_get.side_effect = requests.exceptions.ConnectionError()

        with pytest.raises(requests.exceptions.ConnectionError):

            api_extraction()



    # Test invalid JSON
    @patch("src.ingestion.extract.requests.get")
    def test_api_extraction_invalid_json(self, mock_get):

        mock_response = Mock()

        mock_response.status_code = 200

        mock_response.raise_for_status.return_value = None

        mock_response.json.side_effect = requests.exceptions.JSONDecodeError(
            "Invalid JSON",
            "",
            0
        )

        mock_get.return_value = mock_response

        with pytest.raises(requests.exceptions.JSONDecodeError):

            api_extraction()



    # Test your returned structure
    @patch("src.ingestion.extract.requests.get")
    def test_extraction_schema(self, mock_get):

        mock_response = Mock()

        mock_response.status_code = 200

        mock_response.raise_for_status.return_value = None

        mock_response.json.return_value = {}

        mock_get.return_value = mock_response

        data = api_extraction()

        expected_keys = {
            "geocoding",
            "adzuna",
            "arbeitnow",
            "remotive"
        }

        assert set(data.keys()) == expected_keys