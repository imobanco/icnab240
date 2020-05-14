from ...utils import CNABLinesTestCase
from pyCNAB240.constants import MAIN_FIELDS
from pyCNAB240.pipe_and_filter.set import set_trailer_de_lote


class SetTrailerDeLoteTestCase(CNABLinesTestCase):
    def test_set_trailer_de_lote_1(self):
        expected = "03300015#########000008@@@@@@@@@@@@@@@@@@@@@@@@@@@@"

        fields = set_trailer_de_lote(MAIN_FIELDS)

        result = self.build_result(fields)[-2][:51]

        self.assertEqual(expected, result)

    def test_set_trailer_de_lote_2(self):
        expected = "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"

        fields = set_trailer_de_lote(MAIN_FIELDS)

        result = self.build_result(fields)[-2][51:104]

        self.assertEqual(expected, result)

    def test_set_trailer_de_lote_3(self):
        expected = "@@@@@@@@@@@@@@@@@@@######################################"

        fields = set_trailer_de_lote(MAIN_FIELDS)

        result = self.build_result(fields)[-2][104:161]

        self.assertEqual(expected, result)

    def test_set_trailer_de_lote_4(self):
        expected = "###############################################################################\n"

        fields = set_trailer_de_lote(MAIN_FIELDS)

        result = self.build_result(fields)[-2][161:]

        self.assertEqual(expected, result)
