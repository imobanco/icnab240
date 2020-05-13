from freezegun import freeze_time

from ...utils import CNABLinesTestCase
from pyCNAB240.pipe_and_filter.set import set_header_de_arquivo


class SetHeaderDeArquivoTestCase(CNABLinesTestCase):
    def test_set_header_de_arquivo_1(self):
        expected = "03300000#########200002238490226###################"

        with freeze_time("2020-04-22 18:21:33"):
            fields = set_header_de_arquivo(self._fields, self.header_de_arquivo)

        result = self.build_result(fields)[0][:51]

        self.assertEqual(expected, result)

    def test_set_header_de_arquivo_2(self):
        expected = "300004500000000000678############Um nome de empresa"

        with freeze_time("2020-04-22 18:21:33"):
            fields = set_header_de_arquivo(self._fields, self.header_de_arquivo)

        result = self.build_result(fields)[0][51:102]

        self.assertEqual(expected, result)

    def test_set_header_de_arquivo_3(self):
        expected = "###############Banco Santander##########"

        with freeze_time("2020-04-22 18:21:33"):
            fields = set_header_de_arquivo(self._fields, self.header_de_arquivo)

        result = self.build_result(fields)[0][102:142]

        self.assertEqual(expected, result)

    def test_set_header_de_arquivo_4(self):
        expected = "12204202018213300001401501600"

        with freeze_time("2020-04-22 18:21:33"):
            fields = set_header_de_arquivo(self._fields, self.header_de_arquivo)

        result = self.build_result(fields)[0][142:171]

        self.assertEqual(expected, result)

    def test_set_header_de_arquivo_5(self):
        expected = (
            "#####################################################################\n"
        )

        with freeze_time("2020-04-22 18:21:33"):
            fields = set_header_de_arquivo(self._fields, self.header_de_arquivo)

        result = self.build_result(fields)[0][171:]

        self.assertEqual(expected, result)
