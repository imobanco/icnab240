from freezegun import freeze_time

from ...utils import CNABLinesTestCase
from icnab240.pipe_and_filter.set import set_header_de_arquivo


class SetHeaderDeArquivoTestCase(CNABLinesTestCase):
    def test_set_header_de_arquivo_1(self):
        expected = (
            f"03300000#########2"
            f"{self.header_de_arquivo.get('06.0')}"
            f"###################"
        )

        fields = self._main_fields

        with freeze_time("2020-04-22 18:21:33"):
            set_header_de_arquivo(fields, self.header_de_arquivo)

        result = self.build_result(fields)[0][:51]

        self.assertEqual(expected, result)

    def test_set_header_de_arquivo_2(self):
        expected = (
            f"{self.header_de_arquivo.get('07.0')}"
            f"0000"
            f"{self.header_de_arquivo.get('08.0')}"
            f"{self.header_de_arquivo.get('09.0')}"
            f"00000000000"
            f"{self.header_de_arquivo.get('10.0')}"
            f"{self.header_de_arquivo.get('11.0')}"
            f"{self.header_de_arquivo.get('12.0')}"
            f"############"
            f"{self.header_de_arquivo.get('13.0')}"
        )

        fields = self._main_fields

        with freeze_time("2020-04-22 18:21:33"):
            set_header_de_arquivo(fields, self.header_de_arquivo)

        result = self.build_result(fields)[0][51:102]

        self.assertEqual(expected, result)

    def test_set_header_de_arquivo_3(self):
        expected = (
            f"###############" f"{self.header_de_arquivo.get('14.0')}" f"##########"
        )

        fields = self._main_fields

        with freeze_time("2020-04-22 18:21:33"):
            set_header_de_arquivo(fields, self.header_de_arquivo)

        result = self.build_result(fields)[0][102:142]

        self.assertEqual(expected, result)

    def test_set_header_de_arquivo_4(self):
        expected = (
            f"{self.header_de_arquivo.get('16.0')}"
            f"220420201821330000"
            f"{self.header_de_arquivo.get('19.0')}"
            f"0"
            f"{self.header_de_arquivo.get('20.0')}"
            f"01600"
        )

        fields = self._main_fields

        with freeze_time("2020-04-22 18:21:33"):
            set_header_de_arquivo(fields, self.header_de_arquivo)

        result = self.build_result(fields)[0][142:171]

        self.assertEqual(expected, result)

    def test_set_header_de_arquivo_5(self):
        expected = (
            "#####################################################################\n"
        )

        fields = self._main_fields

        with freeze_time("2020-04-22 18:21:33"):
            set_header_de_arquivo(fields, self.header_de_arquivo)

        result = self.build_result(fields)[0][171:]

        self.assertEqual(expected, result)
