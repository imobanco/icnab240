from ...utils import CNABLinesTestCase
from pyCNAB240.pipe_and_filter.set import set_trailer_de_lote


class SetTrailerDeLoteTestCase(CNABLinesTestCase):
    def test_set_trailer_de_lote_1(self):
        total_lines_1_2_3_4_5 = "000008"

        expected = (
            "03300015#########"
            f"{total_lines_1_2_3_4_5}"
            "@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
        )

        fields = self._main_fields
        set_trailer_de_lote(fields)

        result = self.build_result(fields)[-2][:51]

        self.assertEqual(expected, result)

    def test_set_trailer_de_lote_2(self):
        expected = "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"

        fields = self._main_fields
        set_trailer_de_lote(fields)

        result = self.build_result(fields)[-2][51:104]

        self.assertEqual(expected, result)

    def test_set_trailer_de_lote_3(self):
        expected = "@@@@@@@@@@@@@@@@@@@######################################"

        fields = self._main_fields
        set_trailer_de_lote(fields)

        result = self.build_result(fields)[-2][104:161]

        self.assertEqual(expected, result)

    def test_set_trailer_de_lote_4(self):
        expected = "###############################################################################\n"

        fields = self._main_fields
        set_trailer_de_lote(fields)

        result = self.build_result(fields)[-2][161:]

        self.assertEqual(expected, result)
