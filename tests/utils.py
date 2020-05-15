import os
import json
import unittest

from pyCNAB240.controllers.common import common_initial_controller
from pyCNAB240.pipe_and_filter.build import (
    build_main_fields,
    build_cnab_lines,
    build_pieces_of_value_to_cnab,
)
from pyCNAB240.pipe_and_filter.set import set_fill_value_to_cnab


class CNABLinesTestCase(unittest.TestCase):
    def setUp(self):
        super().setUp()

        self.header_de_arquivo = self.full_file_name("header_de_arquivo.json")
        with open(self.header_de_arquivo) as f:
            self.header_de_arquivo = json.load(f)

        self.header_de_lote = self.full_file_name("header_de_arquivo_lote.json")
        with open(self.header_de_lote) as f:
            self.header_de_lote = json.load(f)

        self._main_fields = build_main_fields()
        NÚMERO_LOTE_DE_SERVIÇO = 1  # G002
        common_initial_controller(self._main_fields, NÚMERO_LOTE_DE_SERVIÇO)

    @staticmethod
    def full_file_name(file_name):
        return os.path.join(os.path.dirname(__file__), file_name)

    @staticmethod
    def build_result(fields):
        set_fill_value_to_cnab(fields)
        pieces = build_pieces_of_value_to_cnab(fields)
        result = build_cnab_lines(pieces)
        return result
