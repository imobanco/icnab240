import unittest

from icnab240.core import Field
from icnab240.pipe_and_filter.count import count_cnab_lines_1_2_3_4_5


class CNABTestCase(unittest.TestCase):
    def test_count_cnab_lines_1_2_3_4_5(self):
        # Note: if default=0 or default=9 it must not be counted
        fields = [
            Field(start=8, end=8, default=1),
            Field(start=8, end=8, default=2),
            Field(start=8, end=8, default=3),
            Field(start=8, end=8, default=4),
            Field(start=8, end=8, default=5),
            Field(start=8, end=8, default=0),
            Field(start=8, end=8, default=9),
        ]

        expected_value = 5
        result = count_cnab_lines_1_2_3_4_5(fields)

        self.assertEqual(expected_value, result)
