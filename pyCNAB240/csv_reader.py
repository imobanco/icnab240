import csv
import os

from csv import DictReader
from csv import reader


def build_list_from_csv(csv_file_name, mode='r', delimiter=','):
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


def read(csv_file_name, mode='r'):
    with open(csv_file_name, mode) as read_obj:
        # Skip header (first line with coments)
        next(read_obj)
        csv_dict_reader = DictReader(read_obj)
        # return = csv_dict_reader
        return [row for row in csv_dict_reader][0]


def read_h(csv_file_name, mode='r'):
    with open(csv_file_name, mode) as read_obj:
        csv_reader = reader(read_obj)
        return [row for row in csv_reader]


def build_dict_from_lines(lines):
    d = {line[1]: line[2] for line in lines}
    return d


def build_dict_from_csv(csv_full_file_name):
    lines = read_h(csv_full_file_name)
    return build_dict_from_lines(lines)


# path_to_diretory = os.path.dirname(__file__)
# csv_full_file_name = os.path.join(path_to_diretory, 'data_header_de_arquivo.csv')
#
# lines = read_h(csv_full_file_name)
# build_dict_from_lines(lines)
# print(build_dict_from_lines(lines))

