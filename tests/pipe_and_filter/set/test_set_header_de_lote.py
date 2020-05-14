from freezegun import freeze_time

from ...utils import CNABLinesTestCase
from pyCNAB240.constants import MAIN_FIELDS
from pyCNAB240.pipe_and_filter.filter import filter_segment
from pyCNAB240.pipe_and_filter.set import set_header_de_lote


class SetHeaderDeLoteTestCase(CNABLinesTestCase):
    def test_set_header_de_lote_1(self):
        expected = "03300011E01##030#1000000140154558###################"

        fields = filter_segment(MAIN_FIELDS, ".1")

        with freeze_time("2020-04-23"):
            fields = set_header_de_lote(fields, self.header_de_lote)

        result = self.build_result(fields)[0][:52]

        self.assertEqual(expected, result)

    def test_set_header_de_lote_2(self):
        expected = "300004500000000000678############"

        fields = filter_segment(MAIN_FIELDS, ".1")

        with freeze_time("2020-04-23"):
            fields = set_header_de_lote(fields, self.header_de_lote)

        result = self.build_result(fields)[0][52:85]

        self.assertEqual(expected, result)

    def test_set_header_de_lote_3(self):
        expected = "Um nome de empresa########################################"

        fields = filter_segment(MAIN_FIELDS, ".1")

        with freeze_time("2020-04-23"):
            fields = set_header_de_lote(fields, self.header_de_lote)

        result = self.build_result(fields)[0][85:143]

        self.assertEqual(expected, result)

        "999999992304202000000000#################################\n"

    def test_set_header_de_lote_4(self):
        expected = "########################################"

        fields = filter_segment(MAIN_FIELDS, ".1")

        with freeze_time("2020-04-23"):
            fields = set_header_de_lote(fields, self.header_de_lote)

        result = self.build_result(fields)[0][143:183]

        self.assertEqual(expected, result)

    def test_set_header_de_lote_5(self):
        expected = "999999992304202000000000#################################\n"

        fields = filter_segment(MAIN_FIELDS, ".1")

        with freeze_time("2020-04-23"):
            fields = set_header_de_lote(fields, self.header_de_lote)

        result = self.build_result(fields)[0][183:]

        self.assertEqual(expected, result)
