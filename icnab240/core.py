import json
import os

from pydantic.dataclasses import dataclass


@dataclass
class Field:
    """

    https://stackoverflow.com/a/55910982
    """

    default: str = None
    end: int = None
    identifier: str = None
    full_name: str = None
    length: int = None
    num_decimals: str = None
    num_or_str: str = None
    reasonable_default: str = None
    start: int = None

    # pad_content: str = None
    # pad_direction: str = None
    # raw_write_default_value: str = None
    # raw_write_value: str = None
    # readed_from_cnab_value: str = None
    # readed_from_cnab_value_cleaned: str = None
    # required: str = None
    value: str = None
    value_to_cnab: str = None
