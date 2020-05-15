from ..core import Field


def build_list_of_fields(data: list):
    """
    Constrói uma lista de :class:`.Field` utilizando o :attr:`data`.

    Args:
        data: lista de dicionários

    Returns:
        lista construída
    """
    fields = []
    for entry in data:
        # Ugly, but only here, and only once, we can survive it ...
        fields.append(Field(**entry))
    return fields


def build_main_fields():
    """
    Constroi a lista de :attr:`.MAIN_FIELDS`.

    Returns:
        lista de campos principais
    """
    import os
    import json

    path_to_pipe_and_filter_diretory = os.path.dirname(__file__)

    file_path = os.path.join(
        path_to_pipe_and_filter_diretory, "..", "data", "reformated_main_full_defaults.json"
    )

    with open(file_path) as f:
        data = json.load(f)

    return build_list_of_fields(data)


def build_pieces_of_value_to_cnab(fields):
    """
    Extraí o valor do :attr:`.value_to_cnab` e adiciona uma
    quebra de linha caso o :attr:`.end` seja 240 (no caso final da linha).

    Args:
        fields: lista de campos

    Returns:
        lista na qual cada elemento é uma string com pelo menos :attr:`.value_to_cnab`
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
    """
    Junta as strings baseado no '\n' e forma um elemento de lista de linhas


    Args:
        pieces: lista na qual cada elemento é uma string e que alguns acabam com '\n'

    Returns:
        lista na qual cada elemento acaba com '\n'
    """
    glued_lines = []
    line = ""
    for piece in pieces:
        line += piece
        if "\n" in piece:
            glued_lines.append(line)
            line = ""
    return glued_lines
