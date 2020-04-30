import csv
import os

from csv import DictReader
from csv import reader


def build_list_from_csv(csv_file_name, mode='r', delimiter=','):
    """

    :param csv_file_name: str with the cvs file name
    :param mode: mode of opening the given file
    :param delimiter: the delimiter
    :return: a list of lines in that each line is a cvs row
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
        return [row for row in csv_dict_reader][0]


def read_horizontaly(csv_file_name, mode='r'):
    with open(csv_file_name, mode) as read_obj:
        csv_reader = reader(read_obj)
        return [row for row in csv_reader]


def read_build_dictreader(csv_file_name, mode='r'):
    with open(csv_file_name, mode) as read_obj:
        # pass the file object to DictReader() to get the DictReader object
        next(read_obj)
        dict_reader = DictReader(read_obj)
        # get a list of dictionaries from dct_reader
        list_of_dict = list(dict_reader)
        return list_of_dict


def build_dict_from_list_of_dictreader(dict_readers):
    """
    d = [{'a': 'x', 'b': 'y', 'c': 'z'}, {'a': 'j', 'c': 'z'}]
    Adapted form:
    https://stackoverflow.com/a/45649266
    :param dict_readers: list of DictReader
    :return: dict in that each key has a list of data from the DictReader values
    """

    d = {key: [dict_r.get(key) for dict_r in dict_readers]
         for key in set().union(*dict_readers)}

    return d


def number_of_lines_in_csv(file_name):
    with open(file_name, mode='r') as f:
        return sum(1 for line in f) - 2


def build_dict_from_lines(lines):
    d = {line[1]: line[2] for line in lines}
    return d


def build_dict_from_csv(csv_full_file_name):
    lines = read_horizontaly(csv_full_file_name)
    return build_dict_from_lines(lines)


def build_dict_from_csv_P_Q_R(csv_full_file_name):
    ...




# path_to_diretory = os.path.dirname(__file__)
# csv_full_file_name = os.path.join(path_to_diretory, 'data_header_de_arquivo.csv')
# csv_full_file_name = os.path.join(path_to_diretory, 'data_segmentos_P_Q_R.csv')

# lines = read_horizontaly(csv_full_file_name)

# lines = read(csv_full_file_name)
#
# dictreaders = read_build_dictreader(csv_full_file_name)
# d = build_dict_from_list_of_dictreader(dictreaders)

# print(d)
# print(number_of_lines_in_csv(csv_full_file_name))
# build_dict_from_lines(lines)
# print(build_dict_from_lines(lines))

