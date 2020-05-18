from ..pipe_and_filter.check import check_start_and_end, check_duplicated_identifiers
from ..pipe_and_filter.set import (
    set_registry_type,
    set_reasonable_default_for_all,
    set_numero_do_lote_de_servico_header_and_footer,
    set_numero_do_lote_de_servico_not_header_footer,
    set_default_value,
    set_spaces_if_it_is_not_retorno,
)


def common_initial_controller(fields, NÚMERO_LOTE_DE_SERVIÇO):
    """
    Essa função possui um 'fluxo' padrão que é compartilhado entre
    os CNAB's de todos os bancos (Santander, Itau e etc...)
    """

    check_start_and_end(fields)
    check_duplicated_identifiers(fields)

    set_registry_type(fields)

    set_reasonable_default_for_all(fields)

    # TODO essas funções devem ter que ser chamadas
    #  depois da inserção dos segmentos P, Q, e R para
    #  que elas possam agir nos campos criados.
    set_numero_do_lote_de_servico_header_and_footer(fields, str(NÚMERO_LOTE_DE_SERVIÇO))
    set_numero_do_lote_de_servico_not_header_footer(fields)

    # TODO: documentar essa função melhor
    set_spaces_if_it_is_not_retorno(fields)

    set_default_value(fields)
