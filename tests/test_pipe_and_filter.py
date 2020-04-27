import mock
import unittest

# import datetime
from datetime import datetime

from freezegun import freeze_time

# TODO: checar qual main_fields esta sendo usada aqui
from pyCNAB240.core import Field, main_fields
from pyCNAB240.pipe_and_filter import *


class CNABLinesTestCase(unittest.TestCase):

    def test_set_header_de_arquivo_1(self):
        expected = '03300000#########200002238490226###################'

        file_name = 'header_de_arquivo_fields.csv'
        path_to_diretory = os.path.dirname(__file__)
        full_file_name = os.path.join(path_to_diretory, file_name)

        fields = filter_segment(main_fields, '.0')

        with freeze_time('2020-04-22 18:21:33'):
            fields = set_header_de_arquivo(fields, full_file_name)

        fields = fill_value_to_cnab(fields)
        pieces = build_pieces_of_value_to_cnab(fields)
        result = build_cnab_lines(pieces)[0][:51]

        self.assertEqual(expected, result)

    def test_set_header_de_arquivo_2(self):
        expected = '300004500000000000678#############################9'

        file_name = 'header_de_arquivo_fields.csv'
        path_to_diretory = os.path.dirname(__file__)
        full_file_name = os.path.join(path_to_diretory, file_name)

        fields = filter_segment(main_fields, '.0')

        with freeze_time('2020-04-22 18:21:33'):
            fields = set_header_de_arquivo(fields, full_file_name)

        fields = fill_value_to_cnab(fields)
        pieces = build_pieces_of_value_to_cnab(fields)
        result = build_cnab_lines(pieces)[0][51:102]

        self.assertEqual(expected, result)

    def test_set_header_de_arquivo_3(self):
        expected = '############################10##########'

        file_name = 'header_de_arquivo_fields.csv'
        path_to_diretory = os.path.dirname(__file__)
        full_file_name = os.path.join(path_to_diretory, file_name)

        fields = filter_segment(main_fields, '.0')

        with freeze_time('2020-04-22 18:21:33'):
            fields = set_header_de_arquivo(fields, full_file_name)

        fields = fill_value_to_cnab(fields)
        pieces = build_pieces_of_value_to_cnab(fields)
        result = build_cnab_lines(pieces)[0][102:142]

        self.assertEqual(expected, result)


    def test_set_header_de_arquivo_4(self):
        expected = '12204202018213300001401501600'

        file_name = 'header_de_arquivo_fields.csv'
        path_to_diretory = os.path.dirname(__file__)
        full_file_name = os.path.join(path_to_diretory, file_name)

        fields = filter_segment(main_fields, '.0')

        with freeze_time('2020-04-22 18:21:33'):
            fields = set_header_de_arquivo(fields, full_file_name)

        fields = fill_value_to_cnab(fields)
        pieces = build_pieces_of_value_to_cnab(fields)
        result = build_cnab_lines(pieces)[0][142:171]

        self.assertEqual(expected, result)

    def test_set_header_de_arquivo_5(self):
        expected = '#####################################################################\n'

        file_name = 'header_de_arquivo_fields.csv'
        path_to_diretory = os.path.dirname(__file__)
        full_file_name = os.path.join(path_to_diretory, file_name)

        fields = filter_segment(main_fields, '.0')

        with freeze_time('2020-04-22 18:21:33'):
            fields = set_header_de_arquivo(fields, full_file_name)

        fields = fill_value_to_cnab(fields)
        pieces = build_pieces_of_value_to_cnab(fields)
        result = build_cnab_lines(pieces)[0][171:]

        self.assertEqual(expected, result)

    def test_set_header_de_lote_1(self):
        expected = '03300011E01##030#1000000140154558###################'

        file_name = 'header_de_arquivo_lote_fields.csv'
        path_to_diretory = os.path.dirname(__file__)
        full_file_name = os.path.join(path_to_diretory, file_name)

        fields = filter_segment(main_fields, '.1')

        with freeze_time('2020-04-23'):
            fields = set_header_de_lote(fields, full_file_name)

        fields = fill_value_to_cnab(fields)
        pieces = build_pieces_of_value_to_cnab(fields)
        result = build_cnab_lines(pieces)[0][:52]

        self.assertEqual(expected, result)

    def test_set_header_de_lote_2(self):
        expected = '300004500000000000678############'

        file_name = 'header_de_arquivo_lote_fields.csv'
        path_to_diretory = os.path.dirname(__file__)
        full_file_name = os.path.join(path_to_diretory, file_name)

        fields = filter_segment(main_fields, '.1')

        with freeze_time('2020-04-23'):
            fields = set_header_de_lote(fields, full_file_name)

        fields = fill_value_to_cnab(fields)
        pieces = build_pieces_of_value_to_cnab(fields)
        result = build_cnab_lines(pieces)[0][52:85]

        self.assertEqual(expected, result)

    def test_set_header_de_lote_3(self):
        expected = 'Um nome de empresa########################################'

        file_name = 'header_de_arquivo_lote_fields.csv'
        path_to_diretory = os.path.dirname(__file__)
        full_file_name = os.path.join(path_to_diretory, file_name)

        fields = filter_segment(main_fields, '.1')

        with freeze_time('2020-04-23'):
            fields = set_header_de_lote(fields, full_file_name)

        fields = fill_value_to_cnab(fields)
        pieces = build_pieces_of_value_to_cnab(fields)
        result = build_cnab_lines(pieces)[0][85:143]

        self.assertEqual(expected, result)

        '999999992304202000000000#################################\n'


    def test_set_header_de_lote_4(self):
        expected = '########################################'

        file_name = 'header_de_arquivo_lote_fields.csv'
        path_to_diretory = os.path.dirname(__file__)
        full_file_name = os.path.join(path_to_diretory, file_name)

        fields = filter_segment(main_fields, '.1')

        with freeze_time('2020-04-23'):
            fields = set_header_de_lote(fields, full_file_name)

        fields = fill_value_to_cnab(fields)
        pieces = build_pieces_of_value_to_cnab(fields)
        result = build_cnab_lines(pieces)[0][143:183]

        self.assertEqual(expected, result)

    def test_set_header_de_lote_5(self):
            expected = '999999992304202000000000#################################\n'

            file_name = 'header_de_arquivo_lote_fields.csv'
            path_to_diretory = os.path.dirname(__file__)
            full_file_name = os.path.join(path_to_diretory, file_name)

            fields = filter_segment(main_fields, '.1')

            with freeze_time('2020-04-23'):
                fields = set_header_de_lote(fields, full_file_name)

            fields = fill_value_to_cnab(fields)
            pieces = build_pieces_of_value_to_cnab(fields)
            result = build_cnab_lines(pieces)[0][183:]

            self.assertEqual(expected, result)

    def test_set_trailer_de_lote(self):
        expected = '03300015#########000008@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#####################################################################################################################\n'

        fields = set_trailer_de_lote(main_fields)

        fields = fill_value_to_cnab(fields)
        pieces = build_pieces_of_value_to_cnab(fields)
        result = build_cnab_lines(pieces)[-2]

        self.assertEqual(expected, result)

    def test_set_trailer_de_arquivo(self):
        expected = '03399999#########000001000010000002#############################################################################################################################################################################################################\n'

        fields = set_trailer_de_arquivo(main_fields)

        fields = fill_value_to_cnab(fields)
        pieces = build_pieces_of_value_to_cnab(fields)
        result = build_cnab_lines(pieces)[-1]

        self.assertEqual(expected, result)

if __name__ == '__main__':
    unittest.main()
