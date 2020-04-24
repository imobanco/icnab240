import os

from datetime import datetime
from pprint import pprint

from pycpfcnpj import cpfcnpj

from pyCNAB240.core import main_fields
from pyCNAB240.csv_reader import build_dict_from_csv


def check_start_and_end(fields):
    """
    Sanity check for start and end values loaded.
    https://stackoverflow.com/a/16789817

    :param fields: a list that each element is type Field
    :return: a list that each element is type Field
    """
    _fields = iter(fields)
    field_old = next(_fields)
    for field in _fields:
        if field_old.end == 240 and field.start == 1:
            field_old = field
            continue

        if field.start - field_old.end != 1:
            raise ValueError(f'Start = {field_old.start} of {field_old.identifier} '
                                f'and end = {field.start} '
                                f'of {field.identifier} are wrong, must differ by 1.')

        field_old = field
    return fields


def check_duplicated_identifiers(fields):
    """Checks duplicated identifiers

    It in fact happened, look 10.3S in the pdf was wrongly repeated.
    :param fields: a list that each element is type Field
    :return: a list that each element is type Field
    """
    set_identifiers = set()
    for field in fields:
        if field.identifier in set_identifiers:
            raise ValueError(f'Duplicated field identifier in {field}')
        else:
            set_identifiers.add(field.identifier)
    return fields


def build_pieces_of_value_to_cnab(fields):
    """Extracts the value in the value_to_cnab field and adds \n as a delimiter
     when field.end == 240, therefore the end of a line

    :param fields: a list that each element is type Field
    :return: a list that each element is a string

    #TODO: check if is necessary convert to str here
    #TODO: trow exception if it has None values? Note str(None) == 'None'
    """
    lines = []

    for field in fields:
        if field.end == 240:
            lines.append(str(field.value_to_cnab) + '\n')
        else:
            lines.append(str(field.value_to_cnab))

    return lines


def build_cnab_lines(pieces):
    """Glues strings finding each \n and form a element of a list of lines

    :param pieces: a list that each element is a string that some are with \n
    :return: a list that each element is a string that ands in \n
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

    :param cnab_file_name: str with the name of the written cnab
    :param lines: list in which each element is a string ending in \n
    :param mode: default mode is write
    :return: None
    """
    with open(cnab_file_name, mode) as file:
        for line in lines:
            file.write(line)


def write_cnab(cnab_file_name, fields):
    """Given a cnab file name and a list of elements type Field write a CNABs_retorno

    :param cnab_file_name: str with the CNABs_retorno file name
    :param fields: a list that each element is type Field
    :return: none
    """
    pieces = build_pieces_of_value_to_cnab(fields)
    lines = build_cnab_lines(pieces)
    _write_cnab(cnab_file_name, lines)


def set_bank_number(fields, bank_number):
    """
    Campo: 01.0, ..., 01.9. All first elements must be set to the bank number.
    Descrição: G001. Sets for all segments, headers and footers
    the same given bank number.

    :param fields: a list that each element is type Field
    :param bank_number: the bank number
    :return: a list that each element is type Field with value
             set to given bank_number
    """
    for field in fields:
        if field.start == 1:
            field.value = bank_number
    return fields


def set_white_spaces(fields):
    """Sets value_to_cnab to spaces if is Alfa and Brancos

    :param fields: a list that each element is type Field
    :return: a list that each element is type Field with value_to_cnab
             set to spaces
    """
    for field in fields:
        if field.num_or_str == 'Alfa' and field.default == 'Brancos':
            field.value_to_cnab = '#'*field.length
            field.value = field.value_to_cnab
    return fields


def set_white_spaces_reasonable_default(fields):
    """Sets value_to_cnab to spaces if is Alfa and Vazio

    :param fields: a list that each element is type Field
    :return: a list that each element is type Field with value_to_cnab
             set to spaces
    """
    for field in fields:
        if field.num_or_str == 'Alfa' and field.reasonable_default == 'Vazio':
            field.value_to_cnab = '#'*field.length
            field.value = field.value_to_cnab
    return fields


def set_zeros_reasonable_default(fields):
    """Sets value_to_cnab to spaces if is Alfa and Vazio

    :param fields: a list that each element is type Field
    :return: a list that each element is type Field with value_to_cnab
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

    :param fields:
    :return:
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


def set_total_lines(fields, total_lines):
    """

    06.9 Quantidade de Registros do Arquivo

    :param fields:
    :param total_lines:
    :return: list of Fields
    """
    for field in fields:
        if field.identifier == '06.9':
            field.value = total_lines
    return fields


def set_registry_type(fields):
    for field in fields:
        if field.start == 8 and field.end == 8:
            field.value_to_cnab = field.default
    return fields


def set_defaults(fields):
    """

    :param fields: a list that each element is type Field
    :return: a list that each element is type Field
    """
    for field in fields:
        if field.default != '' and field.default != 'Brancos':
            field.value = field.default
    return fields


def set_spaces_if_it_is_not_retorno(fields):
    """
    05.5
    Seta no Registro Trailer de Lote se não for do tipo retorno espaços
    em campos que não são usados
    :param fields:
    :return:
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

    :param fields: a list that each element is type Field
    :param value:
    :return: a list that each element is type Field with value field set
             to the given value
    """
    for field in fields:
        if field.start == 4 and field.end == 7 \
            and field.identifier != '02.0' and field.identifier != '02.9':
            field.value = value
    return fields


def set_numero_do_lote_de_servico_not_header_footer(fields):
    """
    Campo: 02.3P, 02.3Q, 02.3R, 02.3S, 02.3T, 02.3U, 02.5
    Descrição: G002

    :param fields:
    :return:
    """
    count = 1
    for field in fields:
        if field.start == 9 and field.end == 13 and field.identifier[-1].isalpha():
            field.value = count
            count += 1

    return fields


# TODO: test and check and remove
def set_lote_de_servico(fields, total_lines):
    """

    06.9 Quantidade de Registros do Arquivo

    :param fields:
    :param total_lines:
    :return: list of Fields
    """
    for field in fields:
        if field.identifier == '06.9':
            field.value = total_lines
    return fields


def count_cnab_lines(fields):
    """Calculates the number of lines the CNABs_retorno has

    :param fields: a list that each element is type Field
    :return: int representing the total of lines that the CNABs_retorno has
    """
    return sum([1 for field in fields if field.end == 240])


def count_cnab_lines_0_1_3_5_9(fields):
    """
    Campo: 06.9
    Descrição: G056 (ver G003 para ver todos tipos de registro)

    :param fields: a list that each element is type Field
    :return: int representing the total of lines 0, 1, 3, 5 and 9 that the CNABs_retorno has
    """
    # Check if it fails ...
    # and field.value in (0, 1, 3, 5, 8)
    return sum([1 for field in fields if field.start == 8
                                         and field.end == 8
                                         ]
               )


def count_cnab_lines_1_2_3_4_5(fields):
    """
    Campo: 05.5
    Descrição: G057 (ver G003 para ver todos tipos de registro)

    :param fields: a list that each element is type Field
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

    :param fields: a list that each element is type Field
    :return: int representing the total of lines of type 1 that the CNABs_retorno has
    """
    return sum([1 for field in fields
                if field.start == 8
                and field.end == 8
                and field.default == '1']
               )


def count_cnab_lines_E(fields):
    """Counts the CNABs lines of type E

    :param fields: a list that each element is type Field
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

    :param fields: a list that each element is type Field
    :return: int representing the total of lines of type 1 and E that the CNABs_retorno has
    """
    return count_cnab_lines_1(fields) + count_cnab_lines_E(fields)


# TODO: after test other functions
def default_decimals(field):
    """
    Vários campos possuem valores decimais
    exemplo: C071

    Não esta claro o que fazer com os campos com 2/5 por hora, C023
    :param field:
    :return: int
    """
    if field.num_decimals == '2':
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

    :param fields: a list that each element is type Field
    :param segment: str to used in the filter
    :return: a list that each element is type Field and was filtered
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

    :param fields: a list that each element is type Field
    :param segment: str to used in the filter
    :return: a list that each element is type Field and was filtered
    """
    fields_filtered = [field for field in fields if segment in field.identifier and field.value is None]
    return fields_filtered


def set_P_Q_R_codigo_de_movimento_remessa(fields, value):
    """
    Campo:
    Código de Movimento Remessa: C004
    :return:
    """
    for field in fields:
        if field.start == 16 and field.end == 17 \
                and field.identifier[-3:] in ('.3P', '.3Q', '.3R'):
            field.value = value

    return fields


def set_P_forma_de_cadastr_do_titulo_no_banco(fields, value):
    """

    Forma de Cadastr. do Título no Banco: *C007

    :param fields:
    :param value:
    :return: List of Fields
    """
    for field in fields:
        if field.identifier == '15.3P':
            field.value = value

    return fields


def set_field(fields, value_to_search, value_to_set):
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
    DEscrição: G005, problema muitos casos diferentes desse campo
    Randomly generated using gen.cpf() from pycpfcnpj:
    00140154558, 00002238490226

    :param fields:
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

    :param fields: a list that each element is type Field
    :param data: dict with keys as identifier and values are the ones provided by
              the user in the .csv file
    :return: a list that each element is type Field with value set to data value
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


BANK_NUMBER = '033'
NÚMERO_LOTE_DE_SERVIÇO = 1 # G002


def generic(main_fields, BANK_NUMBER, NÚMERO_LOTE_DE_SERVIÇO):

    fields = check_start_and_end(main_fields)
    fields = check_duplicated_identifiers(fields)

    fields = set_defaults(fields)

    fields = set_bank_number(fields, BANK_NUMBER)

    fields = set_numero_do_lote_de_servico_header_and_footer(fields, str(NÚMERO_LOTE_DE_SERVIÇO))

    fields = set_numero_do_lote_de_servico_not_header_footer(fields)

    return fields


def set_trailer_de_arquivo(fields):

    total_lines_0_1_3_5_9 = str(count_cnab_lines_0_1_3_5_9(fields))
    total_lines_1_2_3_4_5 = str(count_cnab_lines_1_2_3_4_5(fields))
    total_lines_1 = str(count_cnab_lines_1(fields))
    total_lines_1_and_E_type = str(count_cnab_lines_1_and_E_type(fields))

    fields = set_field(fields, '05.9', total_lines_1)
    fields = set_field(fields, '06.9', total_lines_0_1_3_5_9)
    fields = set_field(fields, '07.9', total_lines_1_and_E_type)
    fields = set_field(fields, '05.5', total_lines_1_2_3_4_5)

    return fields


fields = generic(main_fields, BANK_NUMBER, NÚMERO_LOTE_DE_SERVIÇO)


path_to_diretory = os.path.dirname(__file__)
csv_header_de_arquivo_full_file_name = os.path.join(path_to_diretory, 'data_header_de_arquivo.csv')
fields = set_header_de_arquivo(fields, csv_header_de_arquivo_full_file_name)

path_to_diretory = os.path.dirname(__file__)
csv_header_de_lote_full_file_name = os.path.join(path_to_diretory, 'data_header_de_lote.csv')
fields = set_header_de_lote(fields, csv_header_de_lote_full_file_name)





fields = set_trailer_de_arquivo(fields)


# tanto faz onde for chamado
fields = set_spaces_if_it_is_not_retorno(fields)

fields = set_registry_type(fields)

fields = set_white_spaces(fields)
# print(generic_filter(fields, 'identifier', '04.9'))


# Act in all P, Q and R
fields = set_P_Q_R_codigo_de_movimento_remessa(fields, '1')
fields = set_P_forma_de_cadastr_do_titulo_no_banco(fields, '1')

fields = filter_segment(fields, '.0') + filter_segment(fields, '.1') \
         + filter_segment(fields, '.5') + filter_segment(fields, '.9')


fields = fill_value_to_cnab(fields)

# fields = filter_segment(fields, '.0')
# for field in fields:
#     print(field.identifier, 'length =', field.length, len(field.value_to_cnab), len(field.value), 'value =', field.value, 'value_to_cnab =', field.value_to_cnab)

path_to_diretory = os.path.dirname(__file__)
full_cnab_file_name = os.path.join(path_to_diretory, 'test.REM')
write_cnab(full_cnab_file_name, fields)
