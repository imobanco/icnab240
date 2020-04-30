import os

from pyCNAB240.core import main_fields
from pyCNAB240.pipe_and_filter import santander


BANK_NUMBER = '033'
NÚMERO_LOTE_DE_SERVIÇO = 1 # G002

path_to_diretory = os.path.dirname(__file__)
header_de_arquivo = os.path.join(path_to_diretory, 'header_de_arquivo.csv')
header_de_lote = os.path.join(path_to_diretory, 'header_de_lote.csv')
full_cnab_file_name = os.path.join(path_to_diretory, 'test.REM')


santander(main_fields, BANK_NUMBER, NÚMERO_LOTE_DE_SERVIÇO,
          header_de_arquivo, header_de_lote, full_cnab_file_name)
