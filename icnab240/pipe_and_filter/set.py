import copy
from datetime import datetime

from .check import (
    check_given_data_identifiers,
    check_missing_given_data_identifiers,
    check_size_of_input_data,
    check_overwriting_data,
    check_input_data_type,
)
from .count import (
    count_cnab_lines_1_2_3_4_5,
    count_cnab_lines_0_1_3_5_9,
    count_cnab_lines_1,
    count_cnab_lines_1_E,
)
from .filter import filter_segment
from .utils import default_decimals, inscription_type, index_to_insert
from ..constants import fill_value


def set_default_value(fields):
    """
    Atribui um valor padrão o para :attr:`.value` dos campos.

    Esse valor pode ser um valor: de preenchiento, :attr:`.default` ou :attr:`.reasonable_default`.

    Se o :attr:`.num_or_str` for "Alfa" ou "Num" podemos utilizar um valor de preenchimento
    adequado para o caso. Se for "Num" o preenchimento será "0". Se for "Alfa" (e outras validações) o
    preenchimento será :attr:`.fill_value`

    Se não, precisamos verificar :attr:`.default` e :attr:`.reasonable_default` para decidir
    qual será o preenchimento baseado neles mesmo.

    TODO: listar todos os campos que essa função modifica

    Args:
        fields: campos
    """

    for field in fields:
        if field.num_or_str == "Alfa" and (
            field.default == "Brancos" or field.reasonable_default == "Vazio"
        ):
            field.value = fill_value
        elif field.num_or_str == "Num" and field.reasonable_default == "Vazio":
            field.value = "0"

        elif field.default != "" and field.default != "Brancos":
            field.value = field.default
        elif (
            field.reasonable_default != "Calculavél" and field.reasonable_default != ""
        ):
            field.value = field.reasonable_default


def set_spaces_if_it_is_not_retorno(fields):
    """
    Atribui alguns campos com o :attr:`.fill_value` SE e somente se
    o CNAB não for de retorno.

    O :attr:`.value` "T" indica tipo RETORNO no santander.

    Na listagem abaixo encontram-se os campos em que a função modifica
    e as descrições destes:
    Campos: 06.5, 07.5, 08.5, 09.5, 10.5, 11.5, 12.5, 13.5, 14.5
    Descrição: C070, C071, C072

    Todos os campos listados pertencem ao segmento trailer de lote.
    E por serem em sequência, basta que se filtre no intervalo entre
    começo igual a 24, e fim igual a 116, usando ainda o filtro de
    que seja o segmento trailer de lote, ou seja, que o fim do
    identificador contenha a string .5.

    Attributes:
        fields (lista de :class:`.Field`): campos
    """
    is_retorno = False
    for field in fields:
        if field.start == 9 and field.end == 9 and field.value == "T":
            is_retorno = True

    if not is_retorno:
        for field in fields:
            if 24 <= field.start <= 116 and ".5" in field.identifier:
                field.value = fill_value
                set_fill_value_to_cnab(
                    [field], _custom_fill_value=fill_value, overwrite_value=True
                )


def set_fill_value_to_cnab(fields, _custom_fill_value=None, overwrite_value=False):
    """
    Preenche o :attr:`.value` do campo até o :attr:`.length` com o :attr:`.fill_value`.

    TODO: checar se num_decimals == 2 ou 2/5 interfere em algum caso

    Args:
        fields: campos
        _custom_fill_value: um fill_value customizado
        overwrite_value: flag para sobreescrever o :attr:`.value` com o :attr:`.value_to_cnab`
    """
    for field in fields:
        my_fill_value = None

        if field.value is None:
            field.value = ""
        else:
            field.value = str(field.value)

        total_length = field.length + default_decimals(field)

        if len(field.value) == total_length:
            field.value_to_cnab = field.value
        elif len(field.value) > total_length:
            raise ValueError("Tamanho do valor é maior do que o esperado!")
        else:
            if _custom_fill_value is not None:
                my_fill_value = _custom_fill_value

            if field.num_or_str == "Num":
                length = total_length

                if my_fill_value is None:
                    my_fill_value = "0"
            else:
                length = field.length
                if my_fill_value is None:
                    my_fill_value = fill_value

            field.value_to_cnab = field.value.rjust(length, my_fill_value)

        if overwrite_value:
            field.value = field.value_to_cnab


def set_generic_field(
    fields, attribute_to_search, value_to_search, attribute_to_set, value_to_set
):
    """
    Preenche o :attr:`attribute_to_set` dos :class:`.Field`'s (que são 'batem'
    com o filtro :attr:`value_to_search`) com o valor :attr:`value_to_set`.

    Args:
        fields: campos
        attribute_to_search: nome do atributo que será utilizado na busca
        value_to_search: valor do atributo que será utiliza na busca
        attribute_to_set: nome do atributo que será preenchido
        value_to_set: valor do atributo a ser preenchido
    """
    for field in fields:
        if getattr(field, attribute_to_search) == value_to_search:
            setattr(field, attribute_to_set, value_to_set)


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


def set_numero_do_lote_de_servico_header_and_footer(fields, value):
    """

    Essa função será, muito provavelmente eliminada.
    Ver onde ela é chama!

    Na listagem abaixo encontram-se os campos em que a função modifica
    e as descrições destes:
    Campos: 02.1, 02.9
    Descrição: G002

    E exclui desta modificação os campos: 02.1, 02.9

    O texto da especificação do Santander diz, sobre a descrição G002:
    "Número seqüencial para identificar univocamente um lote de serviço.
    Criado e controlado pelo responsável pela geração magnética dos dados contidos no arquivo.
    Preencher com '0001' para o primeiro lote do arquivo. Para os demais: número do lote
    anterior acrescido de 1. O número não poderá ser repetido dentro do arquivo.".



    :param fields: a list in that each element is type Field
    :param value:
    :return: a list in that each element is type Field with value field set
             to the given value
    """
    for field in fields:
        if (
            field.start == 4
            and field.end == 7
            and field.identifier != "02.0"
            and field.identifier != "02.9"
        ):
            field.value = value


def set_numero_do_lote_de_servico_not_header_footer(fields):
    """
    Campos: 04.3P, 04.3Q, 04.3R, 04.3S, 04.3T, 04.3U
    Descrição: G038

    :param fields: a list in that each element is type Field
    :return: a list that each element is type Field
    """
    count = 1
    for field in fields:
        if field.start == 9 and field.end == 13 and field.identifier[-1].isalpha():
            field.value = count
            count += 1


def set_field(fields, value_to_search, value_to_set):
    """Sets the value_to_set to the field that has identifier equal
    to value_to_search

    :param fields: a list in that each element is type Field
    :param value_to_search: str with the identifier to be searched
    :param value_to_set: str with the value to be set
    :return: a list in that each element is type Field
    """
    for field in fields:
        if field.identifier == value_to_search:
            field.value = value_to_set


def set_cpf_or_cnpj(fields, identifier_inscription_type, identifier_cpf_or_cnpj):
    """Sets in fields if it is cpf of cnpj

    Campos: 06.0, 09.1
    Descrição: G005, problema muitos casos diferentes desse campo
    Randomly generated using gen.cpf() from pycpfcnpj:
    00140154558, 00002238490226

    :param fields: a list in that each element is type Field
    :param identifier_inscription_type: str with identifier of the field inscription type
    :param identifier_cpf_or_cnpj: str with cpf or cnpj number
    :return: a Field with value set that matchs if it is cpf (1) or cnpj (2)
    """
    cpf_or_cnpj = None
    for field in fields:
        if field.identifier == identifier_cpf_or_cnpj:
            cpf_or_cnpj = field.value

    if cpf_or_cnpj is None:
        raise ValueError("Não existe um campo com cpf/cnpj na lista fields")

    for field in fields:
        if field.identifier == identifier_inscription_type:
            field.value = inscription_type(cpf_or_cnpj)


def set_data_to_fields(fields, data):
    """sets given data to fields based on identifiers presents in both

    :param fields: a list in that each element is type Field
    :param data: dict with key as identifier, and value as a list with values
    :return: a list in that each element is type Field, with value set to input data
    """
    for field in fields:
        value = data.get(field.identifier)
        if value is not None:
            value = value.pop(0)
            field.value = value


def set_given_data(fields, data):
    """Sets given data to fields

    :param fields: a list in that each element is type Field
    :param data: dict with keys as identifier and values are the ones provided by
              the user in the .csv file
    :return: a list in that each element is type Field with value set to data value
    """
    for field in fields:
        value = data.get(field.identifier)
        if value is not None:
            field.value = value


def set_header_de_arquivo(fields, data):
    """
    Configura os fields do header de arquivo.

    ..info: Não é uma função pura!!

    ..danger: Essa ação altera os fields!!

    Args:
        fields: lista de campos já existentes
        data: dicionário de input

    """
    check_input_data_type(data)

    # TODO fatorar numa função
    patterns = (".0",)
    check_given_data_identifiers(fields, patterns, data)
    check_missing_given_data_identifiers(fields, patterns, data)
    check_size_of_input_data(fields, data)
    # check_overwriting_data(fields, data)

    set_given_data(fields, data)
    set_cpf_or_cnpj(fields, "05.0", "06.0")

    set_field(fields, "17.0", datetime.today().strftime("%d%m%Y"))
    set_field(fields, "18.0", datetime.today().strftime("%H%M%S"))


def set_header_de_lote(fields, data):
    """
    Configura os fields do header de lote.

    ..info: Não é uma função pura!!

    ..danger: Essa ação altera os fields!!

    Args:
        fields: lista de campos já existentes
        data: dicionário de input

    """

    check_input_data_type(data)

    # TODO check if data has all correct keys
    set_given_data(fields, data)

    set_cpf_or_cnpj(fields, "09.1", "10.1")

    set_field(fields, "21.1", datetime.today().strftime("%d%m%Y"))


def set_trailer_de_lote(fields):

    total_lines_1_2_3_4_5 = str(count_cnab_lines_1_2_3_4_5(fields))

    set_field(fields, "05.5", total_lines_1_2_3_4_5)


def set_trailer_de_arquivo(fields):

    total_lines_0_1_3_5_9 = str(count_cnab_lines_0_1_3_5_9(fields))
    total_lines_1 = str(count_cnab_lines_1(fields))
    total_lines_1_and_e_type = str(count_cnab_lines_1_E(fields))

    set_field(fields, "05.9", total_lines_1)
    set_field(fields, "06.9", total_lines_0_1_3_5_9)
    set_field(fields, "07.9", total_lines_1_and_e_type)


def set_p_q_r(fields, data: dict, patterns, identifier_for_insertion):
    """
    Configura os fields do 'miolo' P, Q e R.

    ..info: Não é uma função pura!!

    ..danger: Essa ação altera os fields!!

    Args:
        fields:
        data:
        patterns:
        identifier_for_insertion:

    Returns:

    """

    check_input_data_type(data)

    # TODO fatorar numa função
    check_given_data_identifiers(fields, patterns, data)
    check_missing_given_data_identifiers(fields, patterns, data)
    check_size_of_input_data(fields, data)
    check_overwriting_data(fields, data)

    number_of_replications = len(next(iter(data.values())))

    set_insert_segments(
        fields, number_of_replications, identifier_for_insertion, patterns
    )

    set_data_to_fields(fields, data)


def set_insert_segments(
    fields, number_of_replications, identifier_for_insertion, patterns
):
    """Insert segments in fields

    Note: it assumes that the given list fields have the replication fields and
          that it appears only once

    :param fields: a list in that each element is type Field
    :param number_of_replications: int representing the number of replications
    :param identifier_for_insertion: str of identifier to the replicated part
                                     be inserted
    :param patterns: iterable with all pattern to be filtered by filter_segment function
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
