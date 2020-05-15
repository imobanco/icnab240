from ...utils import CNABLinesTestCase
from pyCNAB240.pipe_and_filter.set import set_trailer_de_arquivo


class SetTrailerDeArquivoTestCase(CNABLinesTestCase):
    def test_set_trailer_de_arquivo_1(self):
        total_lines_1 = 1
        total_lines_0_1_3_5_9 = 10
        total_lines_1_and_e_type = 2

        expected = (
            "03399999#########00000"
            f"{total_lines_1}"
            "0000"
            f"{total_lines_0_1_3_5_9}"
            "00000"
            f"{total_lines_1_and_e_type}"
        )

        fields = self._main_fields
        set_trailer_de_arquivo(fields)

        result = self.build_result(fields)[-1][:35]

        self.assertEqual(expected, result)

    def test_set_trailer_de_arquivo_2(self):
        expected = "##########################################################"

        fields = self._main_fields
        set_trailer_de_arquivo(fields)

        result = self.build_result(fields)[-1][35 : 35 + 58]

        self.assertEqual(expected, result)

    def test_set_trailer_de_arquivo_3(self):
        expected = "##########################################################"

        fields = self._main_fields
        set_trailer_de_arquivo(fields)

        result = self.build_result(fields)[-1][35 + 58 : 35 + 58 + 58]

        self.assertEqual(expected, result)

    def test_set_trailer_de_arquivo_4(self):
        expected = "##########################################################"

        fields = self._main_fields
        set_trailer_de_arquivo(fields)

        result = self.build_result(fields)[-1][35 + 58 + 58 : 35 + 58 + 58 + 58]

        self.assertEqual(expected, result)

    def test_set_trailer_de_arquivo_5(self):
        expected = "###############################\n"

        fields = self._main_fields
        set_trailer_de_arquivo(fields)

        result = self.build_result(fields)[-1][35 + 58 + 58 + 58 :]
        self.assertEqual(expected, result)
