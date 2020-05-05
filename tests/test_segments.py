import os
import unittest

from freezegun import freeze_time

from pyCNAB240.core import main_fields

from pyCNAB240.pipe_and_filter import filter_segment, generic, \
    set_header_de_arquivo, fill_value_to_cnab, \
    build_pieces_of_value_to_cnab, build_cnab_lines, set_header_de_lote, \
    set_trailer_de_lote, set_trailer_de_arquivo


class CNABLinesTestCase(unittest.TestCase):
    def setUp(self):
        self.header_de_arquivo = self.full_file_name('header_de_arquivo.csv')
        self.header_de_lote = self.full_file_name('header_de_arquivo_lote.csv')

        NÚMERO_LOTE_DE_SERVIÇO = 1  # G002
        self._fields = generic(main_fields, NÚMERO_LOTE_DE_SERVIÇO)

    def full_file_name(self, file_name):
        return os.path.join(os.path.dirname(__file__), file_name)

    def build_result(self, fields):
        fields = fill_value_to_cnab(fields)
        pieces = build_pieces_of_value_to_cnab(fields)
        result = build_cnab_lines(pieces)
        return result

    def test_set_header_de_arquivo_1(self):
        expected = '03300000#########200002238490226###################'

        with freeze_time('2020-04-22 18:21:33'):
            fields = set_header_de_arquivo(self._fields, self.header_de_arquivo)

        result = self.build_result(fields)[0][:51]

        self.assertEqual(expected, result)

    def test_set_header_de_arquivo_2(self):
        expected = '300004500000000000678############Um nome de empresa'

        with freeze_time('2020-04-22 18:21:33'):
            fields = set_header_de_arquivo(self._fields, self.header_de_arquivo)

        result = self.build_result(fields)[0][51:102]

        self.assertEqual(expected, result)

    def test_set_header_de_arquivo_3(self):
        expected = '###############Banco Santander##########'

        with freeze_time('2020-04-22 18:21:33'):
            fields = set_header_de_arquivo(self._fields, self.header_de_arquivo)

        result = self.build_result(fields)[0][102:142]

        self.assertEqual(expected, result)

    def test_set_header_de_arquivo_4(self):
        expected = '12204202018213300001401501600'

        with freeze_time('2020-04-22 18:21:33'):
            fields = set_header_de_arquivo(self._fields, self.header_de_arquivo)

        result = self.build_result(fields)[0][142:171]

        self.assertEqual(expected, result)

    def test_set_header_de_arquivo_5(self):
        expected = '#####################################################################\n'

        with freeze_time('2020-04-22 18:21:33'):
            fields = set_header_de_arquivo(self._fields, self.header_de_arquivo)

        result = self.build_result(fields)[0][171:]

        self.assertEqual(expected, result)

    def test_set_header_de_lote_1(self):
        expected = '03300011E01##030#1000000140154558###################'

        fields = filter_segment(main_fields, '.1')

        with freeze_time('2020-04-23'):
            fields = set_header_de_lote(fields, self.header_de_lote)

        result = self.build_result(fields)[0][:52]

        self.assertEqual(expected, result)

    def test_set_header_de_lote_2(self):
        expected = '300004500000000000678############'

        fields = filter_segment(main_fields, '.1')

        with freeze_time('2020-04-23'):
            fields = set_header_de_lote(fields, self.header_de_lote)

        result = self.build_result(fields)[0][52:85]

        self.assertEqual(expected, result)

    def test_set_header_de_lote_3(self):
        expected = 'Um nome de empresa########################################'

        fields = filter_segment(main_fields, '.1')

        with freeze_time('2020-04-23'):
            fields = set_header_de_lote(fields, self.header_de_lote)

        result = self.build_result(fields)[0][85:143]

        self.assertEqual(expected, result)

        '999999992304202000000000#################################\n'

    def test_set_header_de_lote_4(self):
        expected = '########################################'

        fields = filter_segment(main_fields, '.1')

        with freeze_time('2020-04-23'):
            fields = set_header_de_lote(fields, self.header_de_lote)

        result = self.build_result(fields)[0][143:183]

        self.assertEqual(expected, result)

    def test_set_header_de_lote_5(self):
        expected = '999999992304202000000000#################################\n'

        fields = filter_segment(main_fields, '.1')

        with freeze_time('2020-04-23'):
            fields = set_header_de_lote(fields, self.header_de_lote)

        result = self.build_result(fields)[0][183:]

        self.assertEqual(expected, result)

    def test_set_trailer_de_lote_1(self):
        expected = '03300015#########000008@@@@@@@@@@@@@@@@@@@@@@@@@@@@'

        fields = set_trailer_de_lote(main_fields)

        result = self.build_result(fields)[-2][:51]

        self.assertEqual(expected, result)

    def test_set_trailer_de_lote_2(self):
        expected = '@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@'

        fields = set_trailer_de_lote(main_fields)

        result = self.build_result(fields)[-2][51:104]

        self.assertEqual(expected, result)

    def test_set_trailer_de_lote_3(self):
        expected = '@@@@@@@@@@@@@@@@@@@######################################'

        fields = set_trailer_de_lote(main_fields)

        result = self.build_result(fields)[-2][104:161]

        self.assertEqual(expected, result)

    def test_set_trailer_de_lote_4(self):
        expected = '###############################################################################\n'

        fields = set_trailer_de_lote(main_fields)

        result = self.build_result(fields)[-2][161:]

        self.assertEqual(expected, result)

    def test_set_trailer_de_arquivo_1(self):
        expected = '03399999#########000001000010000002'

        fields = set_trailer_de_arquivo(main_fields)

        result = self.build_result(fields)[-1][:35]

        self.assertEqual(expected, result)

    def test_set_trailer_de_arquivo_2(self):
        expected = '##########################################################'


        fields = set_trailer_de_arquivo(main_fields)

        result = self.build_result(fields)[-1][35:35+58]

        self.assertEqual(expected, result)

    def test_set_trailer_de_arquivo_3(self):
        expected = '##########################################################'

        fields = set_trailer_de_arquivo(main_fields)

        result = self.build_result(fields)[-1][35 + 58:35 + 58 + 58]

        self.assertEqual(expected, result)

    def test_set_trailer_de_arquivo_4(self):
        expected = '##########################################################'

        fields = set_trailer_de_arquivo(main_fields)

        result = self.build_result(fields)[-1][35 + 58 + 58:35 + 58 + 58 + 58]

        self.assertEqual(expected, result)

    def test_set_trailer_de_arquivo_5(self):
        expected = '###############################\n'

        fields = set_trailer_de_arquivo(main_fields)

        result = self.build_result(fields)[-1][35 + 58 + 58 + 58:]
        self.assertEqual(expected, result)
