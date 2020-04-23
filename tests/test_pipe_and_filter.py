import mock
import unittest

from pyCNAB240.core import Field, main_fields
from pyCNAB240.pipe_and_filter import *


class CNABLinesTestCase(unittest.TestCase):
    def test_set_header_de_arquivo(self):
        expected = '03300000#########200002238490226###################300004500000000000678#############################9############################10##########12204202018213300001401501600#####################################################################\n'

        file_name = 'header_de_arquivo_fields.csv'
        path_to_diretory = os.path.dirname(__file__)
        full_file_name = os.path.join(path_to_diretory, file_name)

        fields = filter_segment(main_fields, '.0')

        # TODO: we have to mock: datetime.today().strftime('%d%m%Y') and datetime.today().strftime('%H%M%S')
        fields = set_header_de_arquivo(fields, full_file_name)

        fields = fill_value_to_cnab(fields)
        pieces = build_pieces_of_value_to_cnab(fields)
        result = build_cnab_lines(pieces)[0]

        self.assertEqual(expected, result)


    def test_set_header_de_lote(self):
        expected = '03300011R01##030#1123456789123456#####12345999991234566666234567891245624#########################Pedro####################################### ####################################### 999999990203300401022003#################################\n'

        file_name = 'header_de_arquivo_fields.csv'
        path_to_diretory = os.path.dirname(__file__)
        full_file_name = os.path.join(path_to_diretory, file_name)

        fields = filter_segment(main_fields, '.1')

        fields = set_header_de_arquivo(fields, full_file_name)

        fields = fill_value_to_cnab(fields)
        pieces = build_pieces_of_value_to_cnab(fields)
        result = build_cnab_lines(pieces)[0]

        self.assertEqual(expected, result)

if __name__ == '__main__':
    unittest.main()
