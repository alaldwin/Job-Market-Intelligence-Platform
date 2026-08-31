from pipeline.validation.base_validator import BaseValidator


class AdzunaValidator(BaseValidator):

    REQUIRED_KEYS = [
        "results",
        "count",
    ]

    def validate(self):

        self.validate_not_empty()

        self.validate_type(dict)

        self.validate_required_keys(
            self.REQUIRED_KEYS
        )

        results = self.data["results"]

        if not isinstance(results, list):
            raise TypeError(
                "'results' must be a list."
            )

        for job in results:

            if not isinstance(job, dict):
                raise TypeError(
                    "Each job must be a dictionary."
                )

            required_fields = [
                "id",
                "title",
                "company",
                "location",
            ]

            missing = [
                field
                for field in required_fields
                if field not in job
            ]

            if missing:
                raise ValueError(
                    f"Job missing fields: {missing}"
                )

        return True