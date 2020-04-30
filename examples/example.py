import os

from pyCNAB240.core import main_fields
from pyCNAB240.pipe_and_filter import generic, set_header_de_arquivo, set_header_de_lote, set_trailer_de_lote, \
    set_trailer_de_arquivo, set_P_Q_R_codigo_de_movimento_remessa, set_P_forma_de_cadastr_do_titulo_no_banco, \
    fill_value_to_cnab, write_cnab


BANK_NUMBER = '033'
NÚMERO_LOTE_DE_SERVIÇO = 1 # G002

path_to_diretory = os.path.dirname(__file__)
csv_header_de_arquivo_full_file_name = os.path.join(path_to_diretory, 'header_de_arquivo.csv')
csv_header_de_lote_full_file_name = os.path.join(path_to_diretory, 'header_de_lote.csv')


fields = generic(main_fields, BANK_NUMBER, NÚMERO_LOTE_DE_SERVIÇO)

fields = set_header_de_arquivo(fields, csv_header_de_arquivo_full_file_name)

fields = set_header_de_lote(fields, csv_header_de_lote_full_file_name)

fields = set_trailer_de_lote(fields)

fields = set_trailer_de_arquivo(fields)


# Act in all P, Q and R
fields = set_P_Q_R_codigo_de_movimento_remessa(fields, '1')
fields = set_P_forma_de_cadastr_do_titulo_no_banco(fields, '1')

# fields = filter_segment(fields, '.0') + filter_segment(fields, '.1') \
#          + filter_segment(fields, '.5') + filter_segment(fields, '.9')


fields = fill_value_to_cnab(fields)

# fields = filter_segment(fields, '.0')
# for field in fields:
#     print(field.identifier, 'length =', field.length, len(field.value_to_cnab), len(field.value), 'value =', field.value, 'value_to_cnab =', field.value_to_cnab)

path_to_diretory = os.path.dirname(__file__)
full_cnab_file_name = os.path.join(path_to_diretory, 'test.REM')
write_cnab(full_cnab_file_name, fields)