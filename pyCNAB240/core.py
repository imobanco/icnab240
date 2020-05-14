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


def build_list_of_fields(_data: dict):
    """

    :param dict: a list of lines in which line is a cvs row
    :return: a list that each element is type Field
    """
    fields = []
    for entry in _data:
        # Ugly, but only here, and only once, we can survive it ...
        fields.append(
            Field(**entry)
        )
    return fields


path_to_diretory = os.path.dirname(__file__)
# csv_full_file_name = os.path.join(path_to_diretory, 'data', 'csvs',
#                                   'reformated_main_full.csv')

file_path = os.path.join(
    path_to_diretory, "data", "reformated_main_full_defaults.json"
)

with open(file_path) as f:
    data = json.load(f)

main_fields = build_list_of_fields(data)
