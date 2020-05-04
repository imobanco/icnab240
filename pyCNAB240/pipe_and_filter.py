import os

import copy
from datetime import datetime
from pprint import pprint

from pycpfcnpj import cpfcnpj

from pyCNAB240.core import main_fields
from pyCNAB240.csv_reader import build_dict_from_csv, \
    build_dict_from_csv_P_Q_R, number_of_lines_in_csv


def check_start_and_end(fields):
    """Sanity check for start and end values loaded.

    Checks if all star and end are present, it means
    for all start - end must differ only by 1,
    if end different of 240 and start different of 1

    About the iter and next usage here:
    https://stackoverflow.com/a/16789817

    :param fields: a list in that each element is type Field
    :return: a list in that each element is type Field (just for keep the pattern)
    """
    _fields = iter(fields)
    field_old = next(_fields)
    for field in _fields:
        if field_old.end == 240 and field.start == 1:
            field_old = field
            continue

        if field.start - field_old.end != 1:
            raise ValueError(f'Start = {field_old.start} of '
                             f'{field_old.identifier} and '
                             f'end = {field.start} of {field.identifier}'
                             f'are wrong, must differ by 1.')

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
            raise ValueError(f'Duplicated field identifier in {field}')
        else:
            set_identifiers.add(field.identifier)
    return fields


def build_pieces_of_value_to_cnab(fields):
    """Extracts the value in the value_to_cnab field and adds \n as a hook
     when field.end == 240, therefore the end of a line

    :param fields: a list in that each element is type Field
    :return: a list in that each element is a string with at least value_to_cnab

    #TODO: trow exception if it has None values? Note str(None) == 'None'
    """
    lines = []

    for field in fields:
        if field.end == 240:
            lines.append(field.value_to_cnab + '\n')
        else:
            lines.append(field.value_to_cnab)

    return lines


def build_cnab_lines(pieces):
    """Glues strings finding each \n and form a element of a list of lines

    :param pieces: a list in that each element is a string that some are with \n
    :return: a list in that each element is a string that ands in \n
    """
    glued_lines = []
    line = ''
    for piece in pieces:
        line += piece
        if '\n' in piece:
            glued_lines.append(line)
            line = ''
    return glued_lines


def _write_cnab(cnab_file_name, lines, mode='w'):
    """Helper function that opens and writes a list to a given file name

    :param cnab_file_name: str with the name of the cnab to be written
    :param lines: list in which each element is a string ending in \n
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


def set_bank_number(fields, bank_number):
    """

    TODO: checar como será a construção do arquivo, pois se essa função for
    chamada antes dos segmentos do meio serem criados dará problema.

    Campo: 01.0, ..., 01.9. All first elements must be set to the bank number.
    Descrição: G001. Sets for all segments, headers and footers
    the same given bank number.

    :param fields: a list in that each element is type Field
    :param bank_number: the bank number
    :return: a list in that each element is type Field with value
             set to given bank_number
    """
    for field in fields:
        if field.start == 1:
            field.value = bank_number
    return fields


def set_white_spaces(fields):
    """Sets value_to_cnab to spaces if is Alfa and Brancos

    TODO: listar todos os campos que essa função modifica
    :param fields: a list in that each element is type Field
    :return: a list in that each element is type Field with value_to_cnab
             set to spaces
    """
    for field in fields:
        if field.num_or_str == 'Alfa' and field.default == 'Brancos':
            field.value_to_cnab = '#'*field.length
            field.value = field.value_to_cnab
    return fields


def set_white_spaces_reasonable_default(fields):
    """Sets value_to_cnab to spaces if is Alfa and Vazio

    :param fields: a list in that each element is type Field
    :return: a list in that each element is type Field with value_to_cnab
             set to spaces
    """
    for field in fields:
        if field.num_or_str == 'Alfa' and field.reasonable_default == 'Vazio':
            field.value_to_cnab = '#'*field.length
            field.value = field.value_to_cnab
    return fields


def set_zeros_reasonable_default(fields):
    """Sets value_to_cnab to spaces if is Alfa and Vazio

    :param fields: a list in that each element is type Field
    :return: a list in that each element is type Field with value_to_cnab
             set to spaces

    TODO: checar se num_decimals == 2 ou 2/5 interfere em algum caso
    """
    for field in fields:
        if field.num_or_str == 'Num' and field.reasonable_default == 'Vazio':
            field.value_to_cnab = '0'*field.length
            field.value = field.value_to_cnab
    return fields


def set_reasonable_default_given_values(fields):
    """

    :param fields: a list in that each element is type Field
    :return: a list in that each element is type Field with value set to
             reasonable_default
    """
    for field in fields:
        if field.reasonable_default != 'Vazio' \
                and field.reasonable_default != 'Calculavél':
            field.value = field.reasonable_default
    return fields


def set_generic_field(fields, atribute_to_search, value_to_search,
                      atribute_to_set, value_to_set):
    for field in fields:
        if field.__getattribute__(atribute_to_search) == value_to_search:
            field.__setattr__(atribute_to_set, value_to_set)
    return fields


def generic_filter(fields, atribute_to_search, value_to_search):
    for field in fields:
        if field.__getattribute__(atribute_to_search) == value_to_search:
            return field


def set_registry_type(fields):
    """
    Campos: 03.0, 03.1, 03.P, 03.Q, 03.R, 03.S, 03.T, 03.U, 03.5, 03.9
    # TODO: checar se 03.T, 03.U são escritos em algum momento, ou se são só lidos.
    Descrição: G003

    :param fields: a list in that each element is type Field
    :return: a list in that each element is type Field with
             value_to_cnab set to default
    """
    for field in fields:
        if field.start == 8 and field.end == 8:
            field.value_to_cnab = field.default
    return fields


def set_defaults(fields):
    """

    :param fields: a list in that each element is type Field
    :return: a list in that each element is type Field
    """
    for field in fields:
        if field.default != '' and field.default != 'Brancos':
            field.value = field.default
    return fields


def set_spaces_if_it_is_not_retorno(fields):
    """
    Campos: 05.5
    Seta no Registro Trailer de Lote se não for do tipo retorno espaços
    em campos que não são usados
    :param fields: a list in that each element is type Field
    :return: a list in that each element is type Field
    """
    for field in fields:
        if field.start == 9 and field.end == 9 and field.value == 'T':
            raise ValueError('This function should not be called in this'
                             ' type of CNABs_retorno it is not a RETORNO one.')

    for field in fields:
        if field.start >= 24 and field.start <= 116 \
                and '.5' in field.identifier:

            field.value_to_cnab = '@'*(field.length + default_decimals(field))
            field.value = field.value_to_cnab
            continue

        # if field.identifier == '22.1':
        #     field.value_to_cnab = '@'*(field.length + default_decimals(field))
        #     field.value = field.value_to_cnab

    return fields


def set_numero_do_lote_de_servico_header_and_footer(fields, value):
    """

    Campo: 02.1, 02.9
    Descrição: G002

    :param fields: a list in that each element is type Field
    :param value:
    :return: a list in that each element is type Field with value field set
             to the given value
    """
    for field in fields:
        if field.start == 4 and field.end == 7 \
            and field.identifier != '02.0' and field.identifier != '02.9':
            field.value = value
    return fields


def set_numero_do_lote_de_servico_not_header_footer(fields):
    """
    Campo: 04.3P, 04.3Q, 04.3R, 04.3S, 04.3T, 04.3U
    Descrição: G038

    :param fields: a list in that each element is type Field
    :return: a list that each element is type Field
    """
    count = 1
    for field in fields:
        if field.start == 9 and field.end == 13 and field.identifier[-1].isalpha():
            field.value = count
            count += 1

    return fields


def count_cnab_lines(fields):
    """Calculates the number of lines the CNABs_retorno has

    :param fields: a list in that each element is type Field
    :return: int representing the total of lines that the CNABs_retorno has
    """
    return sum([1 for field in fields if field.end == 240])


def count_cnab_lines_0_1_3_5_9(fields):
    """
    Campo: 06.9
    Descrição: G056 (ver G003 para ver todos tipos de registro)

    :param fields: a list in that each element is type Field
    :return: int representing the total of lines 0, 1, 3, 5 and 9 that the CNABs_retorno has
    """
    # Check if it fails ...
    # and field.value in (0, 1, 3, 5, 8)
    return sum([1 for field in fields if field.start == 8 and field.end == 8])


def count_cnab_lines_1_2_3_4_5(fields):
    """
    Campo: 05.5
    Descrição: G057 (ver G003 para ver todos tipos de registro)

    :param fields: a list in that each element is type Field
    :return: int representing the total of lines 1, 2, 3, 4, and 5 that the CNABs_retorno has
    """
    return sum([1 for field in fields
                if field.start == 8
                and field.end == 8
                and field.default in '12345']
               )


def count_cnab_lines_1(fields):
    """Counts the CNABs lines of type 1

    Campo: 05.9
    Descrição: G049 (ver G003 para ver todos tipos de registro)

    :param fields: a list in that each element is type Field
    :return: int representing the total of lines of type 1 that the CNABs_retorno has
    """
    return sum([1 for field in fields
                if field.start == 8
                and field.end == 8
                and field.default == '1']
               )


def count_cnab_lines_E(fields):
    """Counts the CNABs lines of type E

    :param fields: a list in that each element is type Field
    :return: int representing the total of lines of type E that the CNABs_retorno has
    """
    return sum([1 for field in fields
                if field.start == 9
                and field.end == 9
                and field.value == 'E']
               )


def count_cnab_lines_1_and_E_type(fields):
    """
    Campo: 07.9, uses two other functions to compute all lines type 1 and E

    :param fields: a list in that each element is type Field
    :return: int representing the total of lines of type 1 and E that the CNABs_retorno has
    """
    return count_cnab_lines_1(fields) + count_cnab_lines_E(fields)


def default_decimals(field):
    """
    Vários campos possuem valores decimais
    exemplo: C071, C023

    :param field:
    :return: int
    """
    if field.num_decimals == '2' or field.num_decimals == '2/5':
        return 2
    return 0


def fill_value_to_cnab(fields):
    for field in fields:
        if not isinstance(field.value, str):
            field.value = str(field.value)

        total_length = field.length + default_decimals(field)
        if len(field.value) < total_length:
            if field.num_or_str == 'Num':
                field.value_to_cnab = field.value.zfill(total_length)
            else:
                field.value_to_cnab = field.value.rjust(field.length, '#')
        else:
            field.value_to_cnab = field.value
    return fields


def compose(*args):
    def inner(value):
        final_value = value
        for arg in reversed(args):
            function = arg[0]
            arguments = arg[1:]
            final_value = function(final_value, *arguments)
        return final_value
    return inner


def filter_segment(fields, segment):
    """Filters segments given a string to filter check if on identifier

    :param fields: a list in that each element is type Field
    :param segment: str to used in the filter
    :return: a list in that each element is type Field and was filtered
    """
    fields_filtered = [field for field in fields if segment in field.identifier]
    return fields_filtered


def filter_none(fields):
    fs = []
    for field in fields:
        if field.value is not None and '.5' in field.identifier:
            if 'None' in field.value:
                fs.append(field)
    return fs


def filter_segment_and_value_none(fields, segment):
    """Filters segments given a string to filter check if on identifier

    :param fields: a list in that each element is type Field
    :param segment: str to used in the filter
    :return: a list in that each element is type Field and was filtered
    """
    fields_filtered = [field for field in fields if segment in field.identifier and field.value is None]
    return fields_filtered


# TODO: deletar?
def set_P_Q_R_codigo_de_movimento_remessa(fields, value):
    """
    Campos: 07.3P, 07.3Q, 07.3R. Poderia incluir o 07.3S
    Código de Movimento Remessa: C004

    :param fields: a list in that each element is type Field
    :return: a list in that each element is type Field
    """
    for field in fields:
        if field.start == 16 and field.end == 17 \
                and field.identifier[-3:] in ('.3P', '.3Q', '.3R'):
            field.value = value

    return fields


# TODO: deletar?
def set_P_forma_de_cadastr_do_titulo_no_banco(fields, value):
    """

    Forma de Cadastr. do Título no Banco: *C007

    :param fields: a list in that each element is type Field
    :param value:
    :return: a list in that each element is type Field
    """
    for field in fields:
        if field.identifier == '15.3P':
            field.value = value

    return fields


def set_field(fields, value_to_search, value_to_set):
    """

    :param fields: a list in that each element is type Field
    :param value_to_search:
    :param value_to_set:
    :return: a list in that each element is type Field
    """
    for field in fields:
        if field.identifier == value_to_search:
            field.value = value_to_set

    return fields


def set_reasonable_default(fields, identifier):
    for field in fields:
        if field.identifier == identifier:
            field.value = field.reasonable_default

    return fields


def inscription_type(cpf_or_cnpj):
    """Calculates if string is cpf or cnpj

    Campos: 05.0,
    Descrição: G005

    :param cpf_or_cnpj: str cpf or cnpj
    :return: int, 1 if is cpf, 2 if is cnpj, otherwise raise
    """

    if cpfcnpj.validate(cpf_or_cnpj):
        if len(cpf_or_cnpj) == 11:
            return 1
        else:
            return 2
    else:
        raise ValueError(f'The number is not a valid cpf or cnpj: {cpf_or_cnpj}')


def set_cpf_or_cnpj(fields, identifier_inscription_type,
                    identifier_cpf_or_cnpj):
    """
    Campos: 06.0, 09.1
    Descrição: G005, problema muitos casos diferentes desse campo
    Randomly generated using gen.cpf() from pycpfcnpj:
    00140154558, 00002238490226

    :param fields: a list in that each element is type Field
    :return: a Field with value setted tha mathcs if it is cpf (1) or cnpj (2)
    """
    for field in fields:
        if field.identifier == identifier_cpf_or_cnpj:
            cpf_or_cnpj = field.value

    for field in fields:
        if field.identifier == identifier_inscription_type:
            field.value = inscription_type(cpf_or_cnpj)

    return fields


def set_given_data_to_header_de_arquivo(fields, data):
    """

    :param fields: a list in that each element is type Field
    :param data: dict with keys as identifier and values are the ones provided by
              the user in the .csv file
    :return: a list in that each element is type Field with value set to data value
    """
    for key in data:
        for field in fields:
            if field.identifier == key:
                field.value = data[key]

    return fields


def set_header_de_arquivo(fields, file_name):

    fields = set_reasonable_default(fields, '21.0')

    data = build_dict_from_csv(file_name)
    fields = set_given_data_to_header_de_arquivo(fields, data)
    fields = set_cpf_or_cnpj(fields, '05.0', '06.0')

    fields = set_field(fields, '17.0', datetime.today().strftime('%d%m%Y'))
    fields = set_field(fields, '18.0', datetime.today().strftime('%H%M%S'))

    fields = set_white_spaces_reasonable_default(fields)

    return fields


def set_header_de_lote(fields, file_name):

    # TODO: remover para receber como parâmetro?
    fields = set_reasonable_default(fields, '04.1') # G028 04.1
    data = build_dict_from_csv(file_name)
    fields = set_given_data_to_header_de_arquivo(fields, data)

    fields = set_cpf_or_cnpj(fields, '09.1', '10.1')

    fields = set_field(fields, '21.1', datetime.today().strftime('%d%m%Y'))

    # TODO: talvez fazer uma função só que faz ambas as coisas
    fields = set_white_spaces_reasonable_default(fields)
    fields = set_zeros_reasonable_default(fields)

    return fields


def generic(main_fields, BANK_NUMBER, NÚMERO_LOTE_DE_SERVIÇO):

    fields = check_start_and_end(main_fields)
    fields = check_duplicated_identifiers(fields)

    fields = set_defaults(fields)
    fields = set_registry_type(fields)

    # TODO: remover??
    fields = set_bank_number(fields, BANK_NUMBER)

    fields = set_numero_do_lote_de_servico_header_and_footer(fields, str(NÚMERO_LOTE_DE_SERVIÇO))

    fields = set_numero_do_lote_de_servico_not_header_footer(fields)

    # TODO: documentar essa função melhor
    fields = set_spaces_if_it_is_not_retorno(fields)

    fields = set_white_spaces(fields)

    return fields


def set_trailer_de_lote(fields):

    total_lines_1_2_3_4_5 = str(count_cnab_lines_1_2_3_4_5(fields))

    fields = set_field(fields, '05.5', total_lines_1_2_3_4_5)

    return fields


def set_trailer_de_arquivo(fields):

    total_lines_0_1_3_5_9 = str(count_cnab_lines_0_1_3_5_9(fields))
    total_lines_1 = str(count_cnab_lines_1(fields))
    total_lines_1_and_E_type = str(count_cnab_lines_1_and_E_type(fields))

    fields = set_field(fields, '05.9', total_lines_1)
    fields = set_field(fields, '06.9', total_lines_0_1_3_5_9)
    fields = set_field(fields, '07.9', total_lines_1_and_E_type)

    return fields


def index_to_insert(fields, identifier):
    """Helper function to find a index given a identifier in a list of fields

    Note: the + 1 is for not insert before the item, but after it

    :param fields: a list in that each element is type Field
    :param identifier: str of the identifier of field
    :return: integer representing the index of the given identifier in fields
    """
    index = None
    for i, field in enumerate(fields):
        if field.identifier == identifier:
            index = i
            break
    return index + 1


def insert_segments(fields, number_of_replications, identifier_for_insertion,
                    patterns):
    """Insert segments in fields

    Note: it assumes that the given list fields have the replication fields and
          that it appears only once

    :param fields: a list in that each element is type Field
    :param number_of_replications: int representing the number of replications
    :param identifier_for_insertion: str of identifier to the replicated part
                                     be inserted
    :param patterns: iterable with all pattern to be filtered
    :return: a list in that each element is type Field
    """

    if number_of_replications >= 2:

        filtered_copied_base = []
        for pattern in patterns:
            aux = copy.deepcopy(filter_segment(fields, pattern))
            filtered_copied_base.extend(aux)

        filtered_copied = []
        for _ in range(number_of_replications - 1):
            filtered_copied.extend(copy.deepcopy(filtered_copied_base))

        index = index_to_insert(fields, identifier_for_insertion)
        fields[index:index] = filtered_copied
        return fields

    return fields


def extract_identifiers(fields, patterns):
    filtered_fields = []
    for pattern in patterns:
        filtered_fields.extend(filter_segment(fields, pattern))

    identifiers_list = [field.identifier for field in filtered_fields]

    identifiers = set(identifiers_list)

    return identifiers


def extract_identifiers_that_have_default_or_reasonable_default(fields):
    filtered_fields = []
    for field in fields:
        if (field.reasonable_default is not None and field.reasonable_default != '') or \
                (field.default is not None and field.default != ''):
            filtered_fields.append(field)

    identifiers_list = [field.identifier for field in filtered_fields]

    identifiers = set(identifiers_list)

    return identifiers


def check_given_data_identifiers(fields, patterns, data):
    identifiers_data = set(data.keys())
    identifiers_all = extract_identifiers(fields, patterns)
    identifiers_have_values = extract_identifiers_that_have_default_or_reasonable_default(fields)

    delta = identifiers_all - identifiers_data - identifiers_have_values

    if delta != set():
        raise ValueError(f'Os dados de entrada estão com os campos: {delta} faltando')


def check_overwriting_data(fields, data):
    identifiers_data = set(data.keys())
    identifiers_have_values = extract_identifiers_that_have_default_or_reasonable_default(fields)

    delta = identifiers_data.intersection(identifiers_have_values)

    if delta != set():
        raise ValueError(f'Você está sobre escrevendo os campos: {delta}')


def set_data_to_fields(fields, data):
    """sets given data to fields

    :param fields: a list in that each element is type Field
    :param data: dict with key as identifier, and value as a list with values
    :return: a list in that each element is type Field, with value set to input data
    """
    for key in data:
        values = list(data[key])
        for field in fields:
            if field.identifier == key:
                value = values.pop(0)
                field.value = value

    return fields


def check_size_of_input_data(fields, data):
    for key in data:
        values = list(data[key])
        for field in fields:
            if field.identifier == key:
                expected_size = field.length + default_decimals(field)
                value = values.pop(0)
                if expected_size < len(value):
                    raise ValueError(f'Error in {key}, the value = {value} ')


def set_P_Q_R(fields, csv_full_file_name, patterns, identifier_for_insertion):
    data = build_dict_from_csv_P_Q_R(csv_full_file_name)

    check_given_data_identifiers(fields, patterns, data)
    check_size_of_input_data(fields, data)
    check_overwriting_data(fields, data)

    number_of_replications = number_of_lines_in_csv(csv_full_file_name)


    fields = insert_segments(fields, number_of_replications, identifier_for_insertion,
                             patterns)

    fields = set_data_to_fields(fields, data)

    return fields


def santander(main_fields, BANK_NUMBER, NÚMERO_LOTE_DE_SERVIÇO,
              header_de_arquivo, header_de_lote, csv_file_P_Q_R,
              full_cnab_file_name):

    fields = filter_segment(main_fields, '.0') + filter_segment(main_fields, '.1') \
             + filter_segment(main_fields, '.3P') \
             + filter_segment(main_fields, '.3Q') \
             + filter_segment(main_fields, '.3R') \
             + filter_segment(main_fields, '.5') + filter_segment(main_fields, '.9')

    fields = generic(fields, BANK_NUMBER, NÚMERO_LOTE_DE_SERVIÇO)

    fields = set_header_de_arquivo(fields, header_de_arquivo)

    fields = set_header_de_lote(fields, header_de_lote)

    patterns = ('.3P', '.3Q', '.3R')
    identifier_for_insertion = '29.3R'
    fields = set_P_Q_R(fields, csv_file_P_Q_R, patterns, identifier_for_insertion)

    fields = set_trailer_de_lote(fields)

    fields = set_trailer_de_arquivo(fields)

    fields = fill_value_to_cnab(fields)

    write_cnab(full_cnab_file_name, fields)


# Act in all P, Q and R
# fields = set_P_Q_R_codigo_de_movimento_remessa(fields, '1')
# fields = set_P_forma_de_cadastr_do_titulo_no_banco(fields, '1')

# fields = filter_segment(fields, '.0') + filter_segment(fields, '.1') \
#          + filter_segment(fields, '.5') + filter_segment(fields, '.9')

# fields = filter_segment(fields, '.0')
# for field in fields:
#     print(field.identifier, 'length =', field.length, len(field.value_to_cnab), len(field.value), 'value =', field.value, 'value_to_cnab =', field.value_to_cnab)

