from freezegun import freeze_time

from ...utils import CNABLinesTestCase
from icnab240.pipe_and_filter.filter import filter_segment
from icnab240.pipe_and_filter.set import set_header_de_lote


class SetHeaderDeLoteTestCase(CNABLinesTestCase):
    def test_set_header_de_lote_1(self):
        expected = (
            f"033000"
            f"{self.header_de_lote.get('02.1')}"
            f"1E01##030#10000"
            f"{self.header_de_lote.get('10.1')}"
            f"###################"
        )

        fields = filter_segment(self._main_fields, ".1")

        with freeze_time("2020-04-23"):
            set_header_de_lote(fields, self.header_de_lote)

        result = self.build_result(fields)[0][:52]

        self.assertEqual(expected, result)

    def test_set_header_de_lote_2(self):
        expected = (
            f"{self.header_de_lote.get('11.1')}"
            f"0000"
            f"{self.header_de_lote.get('12.1')}"
            f"{self.header_de_lote.get('13.1')}"
            f"00000000000"
            f"{self.header_de_lote.get('14.1')}"
            f"{self.header_de_lote.get('15.1')}"
            f"{self.header_de_lote.get('16.1')}"
            f"############"
        )

        fields = filter_segment(self._main_fields, ".1")

        with freeze_time("2020-04-23"):
            set_header_de_lote(fields, self.header_de_lote)

        result = self.build_result(fields)[0][52:85]

        self.assertEqual(expected, result)

    def test_set_header_de_lote_3(self):
        expected = (
            f""
            f"{self.header_de_lote.get('17.1')}"
            f"########################################"
        )

        fields = filter_segment(self._main_fields, ".1")

        with freeze_time("2020-04-23"):
            set_header_de_lote(fields, self.header_de_lote)

        result = self.build_result(fields)[0][85:143]

        self.assertEqual(expected, result)

    def test_set_header_de_lote_4(self):
        expected = "########################################"

        fields = filter_segment(self._main_fields, ".1")

        with freeze_time("2020-04-23"):
            set_header_de_lote(fields, self.header_de_lote)

        result = self.build_result(fields)[0][143:183]

        self.assertEqual(expected, result)

    def test_set_header_de_lote_5(self):
        expected = (
            f"{self.header_de_lote.get('20.1')}"
            f"2304202000000000#################################\n"
        )

        fields = filter_segment(self._main_fields, ".1")

        with freeze_time("2020-04-23"):
            set_header_de_lote(fields, self.header_de_lote)

        result = self.build_result(fields)[0][183:]

        self.assertEqual(expected, result)
