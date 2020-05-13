from ..pipe_and_filter.build import build_cnab_lines, build_pieces_of_value_to_cnab


def _write_cnab(cnab_file_name, lines, mode="w"):
    """Helper function that opens and writes a list to a given file name

    :param cnab_file_name: str with the name of the cnab to be written
    :param lines: list in that which each element is a string ending in \n
    :param mode: default mode is write
    :return: None
    """
    with open(cnab_file_name, mode) as file:
        for line in lines:
            file.write(line)


def write_cnab(cnab_file_name, fields):
    """Given a cnab file name and a list of elements type Field write a CNAB

    :param cnab_file_name: str with the CNAB file name
    :param fields: a list in that each element is type Field
    :return: None
    """
    pieces = build_pieces_of_value_to_cnab(fields)
    lines = build_cnab_lines(pieces)
    _write_cnab(cnab_file_name, lines)
