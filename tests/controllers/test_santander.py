import os
import unittest

from freezegun import freeze_time

# from pyCNAB240.constants import MAIN_FIELDS

from pyCNAB240.controllers.santander import santander_controller

from tests.controllers.santander_example import expected_santander


class SantanderTestCase(unittest.TestCase):
    def test_build_santander(self):

        NÚMERO_LOTE_DE_SERVIÇO = 1  # G002

        path_to_diretory = os.path.dirname(__file__)
        header_de_arquivo = os.path.join(path_to_diretory, "header_de_arquivo_2.csv")
        header_de_lote = os.path.join(path_to_diretory, "header_de_lote.csv")
        csv_file_P_Q_R = os.path.join(path_to_diretory, "data_segmentos_P_Q_R.csv")

        with freeze_time("2020-05-05 13:56:45"):
            # https://stackoverflow.com/a/7866180
            delimiter = "\n"
            expecteds = [
                line + delimiter for line in expected_santander.split(delimiter)
            ]

            results = santander_controller(
                NÚMERO_LOTE_DE_SERVIÇO,
                header_de_arquivo,
                header_de_lote,
                csv_file_P_Q_R,
            )

            for line_number, (result, expected) in enumerate(zip(results, expecteds)):
                for index in range(6):
                    with self.subTest():
                        lenght = 40
                        start = index * lenght
                        end = start + lenght
                        msg = f"The line number is {line_number}, and the index is {index}"
                        self.assertEqual(
                            expected[start:end], result[start:end], msg=msg
                        )
