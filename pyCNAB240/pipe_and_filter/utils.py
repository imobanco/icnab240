from pycpfcnpj import cpfcnpj


def compose(*args):
    def inner(value):
        final_value = value
        for arg in reversed(args):
            function = arg[0]
            arguments = arg[1:]
            final_value = function(final_value, *arguments)
        return final_value

    return inner


def default_decimals(field):
    """

    É necessário que se recupere a informação do tamanho do campo
    com base na informação presente na coluna da especificação do Santander
    cujo nome é Nº Dec, que virou no `Field` o atributo `num_decimals`.
    A especificação traz a informação de quantas casas decimais existem
    dessa forma, e isso muda o comprimento do campo. O comprimento do campo
     não é sempre o presente na coluna Nº Dig.
      Se tiver 2 ou 2/5 é necessário que seja adicionado mais dois ao
      comprimento do campo.

    Isso é necessário para que se possa preencher o atributo value_to_cnab
    Examplos de campos que precisam disso são os das descrições: C071, C023

    :param field: Field objecto
    :return: int de acordo com a string no atributo num_decimals
    """
    if field.num_decimals == "2" or field.num_decimals == "2/5":
        return 2
    return 0


def inscription_type(cpf_or_cnpj):
    """Calculates if string is cpf or cnpj

    Campos: 05.0,
    Descrição: G005

    :param cpf_or_cnpj: str cpf or cnpj
    :return: int, 1 if is cpf, 2 if is cnpj, otherwise raise
    """

    if cpfcnpj.cpf.validate(cpf_or_cnpj):
        return 1
    elif cpfcnpj.cnpj.validate(cpf_or_cnpj):
        return 2
    raise ValueError(f"The number is not a valid cpf or cnpj: {cpf_or_cnpj}")


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
