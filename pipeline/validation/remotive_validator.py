from pipeline.validation.base_validator import BaseValidator


class RemotiveValidator(BaseValidator):

    REQUIRED_KEYS = [
        "jobs"
    ]

    def validate(self):

        self.validate_not_empty()

        self.validate_type(dict)

        self.validate_required_keys(
            self.REQUIRED_KEYS
        )

        jobs = self.data["jobs"]

        if not isinstance(jobs, list):
            raise TypeError(
                "'jobs' must be a list."
            )

        for job in jobs:

            if not isinstance(job, dict):
                raise TypeError(
                    "Each job must be a dictionary."
                )

        return True