from pipeline.validation.base_validator import BaseValidator


class ArbeitnowValidator(BaseValidator):

    REQUIRED_KEYS = [
        "data"
    ]

    def validate(self):

        self.validate_not_empty()

        self.validate_type(dict)

        self.validate_required_keys(
            self.REQUIRED_KEYS
        )

        jobs = self.data["data"]

        if not isinstance(jobs, list):
            raise TypeError(
                "'data' must be a list."
            )

        for job in jobs:

            if not isinstance(job, dict):
                raise TypeError(
                    "Each job must be a dictionary."
                )

        return True