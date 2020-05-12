import csv
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


def build_list_from_csv(csv_file_name, mode="r", delimiter=","):
    """

    :param csv_file_name: str with the cvs file name
    :param mode: mode of opening the given file
    :param delimiter: the delimiter
    :return: a list of lines in which line is a cvs row
    """
    with open(csv_file_name, mode=mode) as csv_file:
        reader = csv.reader(csv_file, delimiter=delimiter)
        lines = [row for row in reader]
    return lines


def build_list_of_fields(lines):
    """

    :param lines: a list of lines in which line is a cvs row
    :return: a list that each element is type Field
    """
    fields = []
    for line in lines:
        # Ugly, but only here, and only once, we can survive it ...
        f = Field(
            default=line[7],
            end=line[3],
            identifier=line[0],
            full_name=line[1],
            length=line[4],
            num_decimals=line[5],
            num_or_str=line[6],
            reasonable_default=line[8],
            start=line[2],
        )

        fields.append(f)
    return fields


path_to_diretory = os.path.dirname(__file__)
# csv_full_file_name = os.path.join(path_to_diretory, 'data', 'csvs',
#                                   'reformated_main_full.csv')
csv_full_file_name = os.path.join(
    path_to_diretory, "data", "csvs", "reformated_main_full_defaults.csv"
)

lines = build_list_from_csv(csv_full_file_name)

main_fields = build_list_of_fields(lines)
