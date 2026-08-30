from src.validation.adzuna_validator import (
    AdzunaValidator
)

from src.validation.arbeitnow_validator import (
    ArbeitnowValidator
)

from src.validation.remotive_validator import (
    RemotiveValidator
)

from src.validation.geocoding_validator import (
    GeocodingValidator
)


VALIDATORS = {

    "adzuna": AdzunaValidator,

    "arbeitnow": ArbeitnowValidator,

    "remotive": RemotiveValidator,

    "geocoding": GeocodingValidator,

}


def validate_data(
    source,
    data
):

    validator_cls = VALIDATORS.get(
        source
    )

    if validator_cls is None:
        raise ValueError(
            f"No validator registered "
            f"for {source}"
        )

    validator = validator_cls(
        data
    )

    return validator.validate()