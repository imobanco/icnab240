from .extract import extract_identifiers, extract_identifiers_default
from .utils import default_decimals


def check_start_and_end(fields):
    """Verifica se todos campos do CNAB tem a sequência correta de
    inícios e fins

    De acordo com a especificação do formato do CNAB todo segmento
    começa no indíce 1, e termina no 240, e todo campo tem início
    com este sendo no indíce onde o anterior acabou adicionado de 1.
    Ver a especificação para esclarecimentos.

    Exemplo: o campo 01.0, página 6 do Santander, tem início em 1,
    e término em 3 (o comprimento desse campo é 3 nesse caso),
    portanto o fim deste é 3. O próximo campo, o 02.0, tem início
    em 4, ou seja, o fim do anterior mais 1, e fim neste caso em
    7 (pois o comprimento deste é 4). Esse padrão se mantem, sendo
     apenas diferente no inicio de um segmento, pois o anterior de
     um começo será, se não for o primeiro segmento, o fim do anterior,
     e quando é o fim de um segmento, o fim deste é 240.
    Logo, a diferença entre dois campos consecutivos de um mesmo
      segmento é sempre 1!

    De forma a verificar se a diferença entre dois campos consecutivos de um mesmo
      segmento é sempre 1, é feita uma comparação 2 a 2 na lista de campos utilizando
    o cálculo: `campo_atual.start` - `campo_anterior.end` == 1

    Se esse cálculo falhar há uma inconsistência nos campos, ou seja,
    tem-se algum ou inicio ou fim errado, ou um campo errado, com
     início errado ou fim, ou ainda, por exemplo, um campo na posição
     errada.

    Se `end` é 240 quer dizer que chegou no campo final.
    Se até esse momento o cálculo não falhou então todos os
    campos estão presentes e com 'inícios' e 'fins' corretos para
    um segmento.

    Sobre a função iter e next utilização presente aqui:
    https://stackoverflow.com/a/16789817

    :param fields: uma lista em que cada elemento é do tipo Field
    :return: uma lista em que cada elemento é do tipo Field (não a modifica, apenas checa)
    """
    _fields = iter(fields)
    field_old = next(_fields)
    for field in _fields:
        if field_old.end == 240 and field.start == 1:
            field_old = field
            continue

        if field.start - field_old.end != 1:
            raise ValueError(
                f"Start = {field_old.start} of "
                f"{field_old.identifier} and "
                f"end = {field.start} of {field.identifier}"
                f"are wrong, must differ by 1."
            )

        field_old = field
    return fields


def check_duplicated_identifiers(fields):
    """Checks duplicated identifiers

    It in fact had happened, look 10.3S in the pdf was clearly wrongly repeated.

    :param fields: a list in that each element is type Field
    :return: a list in that each element is type Field (just for keep the pattern)
    """
    set_identifiers = set()
    for field in fields:
        if field.identifier in set_identifiers:
            raise ValueError(f"Duplicated field identifier in {field}")
        else:
            set_identifiers.add(field.identifier)
    return fields


def check_given_data_identifiers(fields, patterns, data):
    """Checks if data has wrong keys passed, even with correct values for the key

    If for some reason data is passed with a typo this function is going to
    raise ValueError.

    :param fields: a list in that each element is type Field
    :param patterns: iterable with all pattern to be filtered by filter_segment function
    :param data: a dict in that each key is a identifier and value is a list wit data
    :return: None
    """
    identifiers_data = set(data.keys())
    identifiers_all = extract_identifiers(fields, patterns)

    for id_data in identifiers_data:
        if id_data not in identifiers_all:
            raise ValueError(f"O identificador do campo: {id_data} esta errado!")


def check_missing_given_data_identifiers(fields, patterns, data):
    """Check if the given data does not have all identifiers that it must have

    If all identifiers of data (for data identifiers are the keys) plus the
    identifiers of fields that have the default or reasonable_default have to
    be equal of the total of identifiers in the fields.

    :param fields: a list in that each element is type Field
    :param patterns: iterable with all pattern to be filtered by filter_segment function
    :param data: a dict in that each key is a identifier and value is a list wit data
    :return: None
    """
    identifiers_data = set(data.keys())
    identifiers_all = extract_identifiers(fields, patterns)
    identifiers_have_values = extract_identifiers_default(fields)

    delta = identifiers_all - identifiers_data - identifiers_have_values

    if delta != set():
        raise ValueError(f"Os dados de entrada estão com os campos: {delta} faltando")


def check_overwriting_data(fields, data):
    """Checks if any identifier in data has already a default
    or reasonable_default repeated in fields

    :param fields: a list in that each element is type Field
    :param data: a dict in that each key is a identifier and value is a list with values
    :return: None
    """
    identifiers_data = set(data.keys())
    identifiers_have_values = extract_identifiers_default(fields)

    delta = identifiers_data.intersection(identifiers_have_values)

    if delta != set():
        raise ValueError(f"Você está sobre escrevendo os campos: {delta}")


def check_size_of_input_data(fields, data):
    """Checks if the inputted data is bigger than the maximum allowed in field

    :param fields: a list in that each element is type Field
    :param data: dict with key as identifier, and value as a list with values
    :return: None
    """
    for key in data:
        values = list(data[key])
        for field in fields:
            if field.identifier == key:
                expected_size = field.length + default_decimals(field)
                value = values.pop(0)
                if expected_size < len(value):
                    raise ValueError(f"Error in {key}, the value = {value} ")


def check_none_value(fields):
    """Checks if the given fields have value None, if so, raise ValueError

    :param fields: a list in that each element is type Field
    :return: None
    """
    for field in fields:
        if field.value is None:
            raise ValueError(f"Error: value = None in {field}")


def check_lines_length(lines, length):
    """

    :param lines: a list in that each element is a string ending in '\n'
    :param length: the number of characters that must be verified
    :return: None
    """
    for line in lines:
        if len(line) != length:
            raise ValueError(f"Error: line length = {len(line)}")


def check_data(fields, patterns, data):
    """
    :param fields: a list in that each element is type Field
    :param patterns:
    :param data:
    :return: None
    """
    check_given_data_identifiers(fields, patterns, data)
    check_missing_given_data_identifiers(fields, patterns, data)
    check_size_of_input_data(fields, data)
    check_overwriting_data(fields, data)


def check_value_type(value):
    """
    Verifica se o valor passado é uma string.
    """
    if isinstance(value, str) and value:
        return
    raise TypeError(
        f"O valor {type(value).__name__}({value}) falhou na validação! Ele precisa ser uma string não vazia!"
    )


def check_input_data_type(data: dict):
    """
    Verifica se todos os campos recebidos no dicionário são strings ou lista de strings.

    :param data: dicionário de informação
    :return: None
    """
    errors = []
    for key, value in data.items():
        try:
            if isinstance(value, list):
                if not value:
                    check_value_type(value)

                for item in value:
                    check_value_type(item)
            else:
                check_value_type(value)
        except TypeError as e:
            errors.append({key: str(e)})

    if errors:
        raise TypeError(errors)
