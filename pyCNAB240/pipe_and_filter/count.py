def count_cnab_lines(fields):
    """Calculates the number of lines the CNAB has

    :param fields: a list in that each element is type Field
    :return: int representing the total of lines that the CNAB has
    """
    return sum([1 for field in fields if field.end == 240])


def count_cnab_lines_0_1_3_5_9(fields):
    """

    Na listagem abaixo encontram-se o(os) campo(os) em que a função modifica
    e a(a)s descrição(ões) deste(es):
    Campo: 06.9
    Descrição: G056 (ver G003 para ver todos tipos de registro)

    Todo o texto da especificação do Santander, sobre a descrição G002, diz:
    "Quantidade de Registros do Arquivo
    Número obtido pela contagem dos registros enviados no arquivo. Somatória dos registros
    de tipo 0, 1, 3, 5 e 9."


    :param fields: uma lista em que cada elemento é do tipo Field
    :return: int representando o total de linhas de tipo 0, 1, 3, 5 e 9 que o CNAB tem
    """
    # TODO: revisar o teste dessa função e incluir casos diferentes e
    # verificar se o atual esta correto.
    # Check if it fails ...
    # and field.value in (0, 1, 3, 5, 8)
    return sum([1 for field in fields if field.start == 8 and field.end == 8])


def count_cnab_lines_1_2_3_4_5(fields):
    """
    TODO: provavelmente no mesmo PR da count_cnab_lines_0_1_3_5_9
    Campo: 05.5
    Descrição: G057 (ver G003 para ver todos tipos de registro)

    :param fields: a list in that each element is type Field
    :return: int representing the total of lines 1, 2, 3, 4, and 5 that the CNABs_retorno has
    """
    return sum(
        [
            1
            for field in fields
            if field.start == 8 and field.end == 8 and field.default in "12345"
        ]
    )


def count_cnab_lines_1(fields):
    """Counts the CNABs lines of type 1

    TODO: provavelmente no mesmo PR da `count_cnab_lines_0_1_3_5_9`.

    Campo: 05.9
    Descrição: G049 (ver G003 para ver todos tipos de registro)

    :param fields: a list in that each element is type Field
    :return: int representing the total of lines of type 1 that the CNAB has
    """
    return sum(
        [
            1
            for field in fields
            if field.start == 8 and field.end == 8 and field.default == "1"
        ]
    )


def count_cnab_lines_E(fields):
    """Counts the CNABs lines of type E

    :param fields: a list in that each element is type Field
    :return: int representing the total of lines of type E that the CNAB has
    """
    return sum(
        [
            1
            for field in fields
            if field.start == 9 and field.end == 9 and field.value == "E"
        ]
    )


def count_cnab_lines_1_and_E_type(fields):
    """
    Campo: 07.9, uses two other functions to compute all lines type 1 and E

    :param fields: a list in that each element is type Field
    :return: int representing the total of lines of type 1 and E that the CNAB has
    """
    return count_cnab_lines_1(fields) + count_cnab_lines_E(fields)

