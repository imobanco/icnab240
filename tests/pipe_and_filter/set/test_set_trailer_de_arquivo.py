from ...utils import CNABLinesTestCase
from pyCNAB240.constants import MAIN_FIELDS
from pyCNAB240.pipe_and_filter.set import set_trailer_de_arquivo


class SetTrailerDeArquivoTestCase(CNABLinesTestCase):
    def test_set_trailer_de_arquivo_1(self):
        expected = "03399999#########000001000010000002"

        fields = set_trailer_de_arquivo(MAIN_FIELDS)

        result = self.build_result(fields)[-1][:35]

        self.assertEqual(expected, result)

    def test_set_trailer_de_arquivo_2(self):
        expected = "##########################################################"

        fields = set_trailer_de_arquivo(MAIN_FIELDS)

        result = self.build_result(fields)[-1][35 : 35 + 58]

        self.assertEqual(expected, result)

    def test_set_trailer_de_arquivo_3(self):
        expected = "##########################################################"

        fields = set_trailer_de_arquivo(MAIN_FIELDS)

        result = self.build_result(fields)[-1][35 + 58 : 35 + 58 + 58]

        self.assertEqual(expected, result)

    def test_set_trailer_de_arquivo_4(self):
        expected = "##########################################################"

        fields = set_trailer_de_arquivo(MAIN_FIELDS)

        result = self.build_result(fields)[-1][35 + 58 + 58 : 35 + 58 + 58 + 58]

        self.assertEqual(expected, result)

    def test_set_trailer_de_arquivo_5(self):
        expected = "###############################\n"

        fields = set_trailer_de_arquivo(MAIN_FIELDS)

        result = self.build_result(fields)[-1][35 + 58 + 58 + 58 :]
        self.assertEqual(expected, result)
