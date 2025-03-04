from typing import Any
import jsonschema
from pytabify.core.dt_schema import DATA_TABLE_SCHEMA

def validate_data(data: Any) -> bool:
    try:
        jsonschema.validate(instance=data, schema=DATA_TABLE_SCHEMA)
        return True
    except jsonschema.ValidationError as e:
        raise e
