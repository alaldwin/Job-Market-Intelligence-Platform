from src.validation.base_validator import BaseValidator


class GeocodingValidator(BaseValidator):

    def validate(self):

        self.validate_not_empty()

        self.validate_type(
            list
        )

        for city in self.data:

            if not isinstance(city, dict):
                raise TypeError(
                    "Each city must be a dictionary."
                )

        return True