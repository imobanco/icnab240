from ..pipe_and_filter.check import (
    check_start_and_end, check_duplicated_identifiers
)
from ..pipe_and_filter.set import (
    set_defaults, set_registry_type,
    set_reasonable_default_for_all, set_white_spaces_reasonable_default,
    set_zeros_reasonable_default, set_numero_do_lote_de_servico_header_and_footer,
    set_numero_do_lote_de_servico_not_header_footer,
    set_white_spaces, set_spaces_if_it_is_not_retorno
)


def common_initial_controller(main_fields, NÚMERO_LOTE_DE_SERVIÇO):
    """
    Essa função possui um 'fluxo' padrão que é compartilhado entre
    os CNAB's de todos os bancos (Santander, Itau e etc...)
    """

    fields = check_start_and_end(main_fields)
    fields = check_duplicated_identifiers(fields)

    fields = set_defaults(fields)
    fields = set_registry_type(fields)

    fields = set_reasonable_default_for_all(fields)
    fields = set_white_spaces_reasonable_default(fields)
    fields = set_zeros_reasonable_default(fields)

    # TODO essas funções devem ter que ser chamadas
    #  depois da inserção dos segmentos P, Q, e R para
    #  que elas possam agir nos campos criados.
    fields = set_numero_do_lote_de_servico_header_and_footer(
        fields, str(NÚMERO_LOTE_DE_SERVIÇO)
    )
    fields = set_numero_do_lote_de_servico_not_header_footer(fields)

    # TODO: documentar essa função melhor
    fields = set_spaces_if_it_is_not_retorno(fields)

    fields = set_white_spaces(fields)

    return fields
