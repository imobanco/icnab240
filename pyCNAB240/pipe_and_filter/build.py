from ..core import Field


def build_list_of_fields(_data: dict):
    """

    :param dict: a list of lines in which line is a cvs row
    :return: a list that each element is type Field
    """
    fields = []
    for entry in _data:
        # Ugly, but only here, and only once, we can survive it ...
        fields.append(Field(**entry))
    return fields


def build_pieces_of_value_to_cnab(fields):
    """Extracts the value in the value_to_cnab field and adds \n as a hook
     when field.end == 240, therefore the end of a line

    :param fields: a list in that each element is type Field
    :return: a list in that each element is a string with at least value_to_cnab

    #TODO: trow exception if it has None values? Note str(None) == 'None'
    """
    lines = []
    # TODO transformar numa string só simplificando a escrita do arquivo.
    for field in fields:
        value = field.value_to_cnab
        if field.end == 240:
            value += "\n"
        lines.append(value)

    return lines


def build_cnab_lines(pieces):
    """Glues strings finding each \n and form a element of a list of lines

    :param pieces: a list in that each element is a string that some end with \n
    :return: a list in that each element is a string that ends in \n
    """
    glued_lines = []
    line = ""
    for piece in pieces:
        line += piece
        if "\n" in piece:
            glued_lines.append(line)
            line = ""
    return glued_lines
