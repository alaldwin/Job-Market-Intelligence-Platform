import json

from common.logger import get_logger

logger = get_logger(
    __name__,
    "validation.log"
)


class BaseValidator:

    def __init__(self, data):
        self.data = data

    def validate_not_empty(self):

        if self.data is None:
            raise ValueError(
                "API response is None."
            )

        if not self.data:
            raise ValueError(
                "API response is empty."
            )

        return True

    def validate_type(self, expected_type):

        if not isinstance(
            self.data,
            expected_type
        ):
            raise TypeError(
                f"Expected {expected_type}, "
                f"got {type(self.data)}"
            )

        return True

    def validate_required_keys(
        self,
        required_keys
    ):

        missing = [
            key
            for key in required_keys
            if key not in self.data
        ]

        if missing:
            raise ValueError(
                f"Missing required keys: {missing}"
            )

        return True