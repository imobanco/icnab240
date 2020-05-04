import os

from pyCNAB240.core import main_fields
from pyCNAB240.csv_reader import build_dict_from_csv_P_Q_R
from pyCNAB240.pipe_and_filter import santander


BANK_NUMBER = '033'
NÚMERO_LOTE_DE_SERVIÇO = 1 # G002

path_to_diretory = os.path.dirname(__file__)
header_de_arquivo = os.path.join(path_to_diretory, 'header_de_arquivo.csv')
header_de_lote = os.path.join(path_to_diretory, 'header_de_lote.csv')
csv_file_P_Q_R = os.path.join(path_to_diretory, 'data_segmentos_P_Q_R.csv')
full_cnab_file_name = os.path.join(path_to_diretory, 'test.REM')


# d = build_dict_from_csv_P_Q_R(csv_file_P_Q_R)
#
# print(d)


santander(main_fields, BANK_NUMBER, NÚMERO_LOTE_DE_SERVIÇO,
          header_de_arquivo, header_de_lote, csv_file_P_Q_R, full_cnab_file_name)
