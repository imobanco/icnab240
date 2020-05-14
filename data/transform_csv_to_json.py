import os
import csv
import json

current_path = os.path.dirname(__file__)

file_name = 'reformated_main_full_defaults'

csv_full_file_name = os.path.join(
    current_path, "csvs", f"{file_name}.csv"
)


def build_list_from_csv(csv_file_name, mode="r", delimiter=","):
    """

    :param csv_file_name: str with the cvs file name
    :param mode: mode of opening the given file
    :param delimiter: the delimiter
    :return: a list of lines in which line is a cvs row
    """
    with open(csv_file_name, mode=mode) as csv_file:
        reader = csv.reader(csv_file, delimiter=delimiter)
        return [row for row in reader]


lines = build_list_from_csv(csv_full_file_name)

json_data = []

for line in lines:
    # Ugly, but only here, and only once, we can survive it ...
    json_data.append(
        {
            "identifier": line[0],
            "full_name": line[1],
            "start": line[2],
            "end": line[3],
            "length": line[4],
            "num_decimals": line[5],
            "num_or_str": line[6],
            "default": line[7],
            "reasonable_default": line[8],
        }
    )

file_path = os.path.join(current_path, f"{file_name}.json")
with open(file_path, "w") as file:
    json.dump(json_data, file, indent=4)
