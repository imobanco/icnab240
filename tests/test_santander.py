import os
import unittest

from freezegun import freeze_time

from pyCNAB240.core import main_fields

from pyCNAB240.pipe_and_filter import build_santander

from tests.santander_example import expected_santander

class SantanderTestCase(unittest.TestCase):

    # def test_test(self):
    #     for i in range(5):
    #         with self.subTest(i=i):
    #             for j in range(10):
    #                 self.assertEqual(i, j)


    def test_santander(self):
        BANK_NUMBER = '033'
        NÚMERO_LOTE_DE_SERVIÇO = 1  # G002

        path_to_diretory = os.path.dirname(__file__)
        header_de_arquivo = os.path.join(path_to_diretory, 'header_de_arquivo_2.csv')
        header_de_lote = os.path.join(path_to_diretory, 'header_de_lote.csv')
        csv_file_P_Q_R = os.path.join(path_to_diretory, 'data_segmentos_P_Q_R.csv')


        with freeze_time('2020-04-22 18:21:33'):
            # https://stackoverflow.com/a/7866180
            delimiter = '\n'
            expecteds = [line + delimiter for line in
                         expected_santander.split(delimiter)]

            results = build_santander(main_fields, BANK_NUMBER,
                                    NÚMERO_LOTE_DE_SERVIÇO, header_de_arquivo,
                                    header_de_lote, csv_file_P_Q_R)

            for line_number, (result, expected) in enumerate(zip(results, expecteds)):
                for index in range(6):
                    with self.subTest(line_number=line_number):
                        self.assertEqual(expected[index:index+30], result[index:index+30])
