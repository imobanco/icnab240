from .common import common_initial_controller
from .file import _write_cnab
from ..pipe_and_filter.build import (
    build_main_fields,
    build_cnab_lines,
    build_pieces_of_value_to_cnab,
)
from ..pipe_and_filter.check import check_none_value, check_lines_length
from ..pipe_and_filter.filter import filter_segment
from ..pipe_and_filter.set import (
    set_header_de_arquivo,
    set_header_de_lote,
    set_p_q_r,
    set_trailer_de_lote,
    set_trailer_de_arquivo,
    set_fill_value_to_cnab,
)


def _santander_controller(
    service_lote_number, header_de_arquivo, header_de_lote, p_q_r,
):

    # TODO: fazer uma função que deleta os segmentos
    main_fields = build_main_fields()
    fields = (
        filter_segment(main_fields, ".0")
        + filter_segment(main_fields, ".1")
        + filter_segment(main_fields, ".3P")
        + filter_segment(main_fields, ".3Q")
        + filter_segment(main_fields, ".3R")
        + filter_segment(main_fields, ".5")
        + filter_segment(main_fields, ".9")
    )

    common_initial_controller(fields, service_lote_number)

    set_header_de_arquivo(fields, header_de_arquivo)

    set_header_de_lote(fields, header_de_lote)

    patterns = (".3P", ".3Q", ".3R")
    identifier_for_insertion = "29.3R"
    set_p_q_r(fields, p_q_r, patterns, identifier_for_insertion)

    set_trailer_de_lote(fields)

    set_trailer_de_arquivo(fields)

    check_none_value(fields)

    set_fill_value_to_cnab(fields)

    # define a function?
    pieces = build_pieces_of_value_to_cnab(fields)
    lines = build_cnab_lines(pieces)
    check_lines_length(lines, 241)

    return lines


def create_santander_cnab(
    service_lote_number, header_de_arquivo, header_de_lote, p_q_r, full_cnab_file_name,
):

    lines = _santander_controller(
        service_lote_number, header_de_arquivo, header_de_lote, p_q_r,
    )

    _write_cnab(full_cnab_file_name, lines)
