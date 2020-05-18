import os
import json

from freezegun import freeze_time

from icnab240.controllers.santander import _santander_controller

from .data.santander_example import expected_santander
from ..utils import MockedFillerTestCase


class SantanderTestCase(MockedFillerTestCase):
    def test_santander_controller(self):

        NÚMERO_LOTE_DE_SERVIÇO = 1  # G002

        path_to_diretory = os.path.dirname(__file__)

        header_de_arquivo = os.path.join(path_to_diretory, "data", "header_de_arquivo_2.json")
        with open(header_de_arquivo) as f:
            header_de_arquivo = json.load(f)

        header_de_lote = os.path.join(path_to_diretory, "data", "header_de_lote.json")
        with open(header_de_lote) as f:
            header_de_lote = json.load(f)

        p_q_r = os.path.join(path_to_diretory, "data", "data_segmentos_P_Q_R.json")
        with open(p_q_r) as f:
            p_q_r = json.load(f)

        with freeze_time("2020-05-05 13:56:45"):
            # https://stackoverflow.com/a/7866180
            delimiter = "\n"
            expecteds = [
                line + delimiter for line in expected_santander.split(delimiter)
            ]

            results = _santander_controller(
                NÚMERO_LOTE_DE_SERVIÇO, header_de_arquivo, header_de_lote, p_q_r,
            )

            for line_number, (result, expected) in enumerate(zip(results, expecteds)):
                for index in range(6):
                    with self.subTest(f"Line: {line_number} && index: {index}"):
                        lenght = 40
                        start = index * lenght
                        end = start + lenght
                        self.assertEqual(expected[start:end], result[start:end])
