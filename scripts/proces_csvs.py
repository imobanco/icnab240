import csv
import json
import os
import re

from pprint import pprint


def load_csv(csv_file_name, out_csv_file_name, delimiter=","):

    lines = []
    with open(csv_file_name, newline="") as csv_file:
        reader = csv.reader(csv_file, delimiter=delimiter)
        for row in reader:
            splited_last_column = row[2].split()
            if len(splited_last_column) < 6:
                splited_last_column.append("")
            lines.append(row[:2] + splited_last_column)
            # print(row[:2] + splited_last_column)

    with open(out_csv_file_name, "w", newline="") as out_csv_file:
        wr = csv.writer(out_csv_file)
        wr.writerows(lines)


csv_file_name = "csvs/main_full.csv"
out_csv_file_name = "csvs/reformated_main_full.csv"

reader = load_csv(csv_file_name, out_csv_file_name)
