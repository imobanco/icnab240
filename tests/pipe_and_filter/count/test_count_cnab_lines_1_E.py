import unittest

from icnab240.core import Field
from icnab240.pipe_and_filter.count import count_cnab_lines_1_E


class CNABTestCase(unittest.TestCase):
    def test_count_cnab_lines_1_and_E_type(self):

        fields = [
            Field(start=8, end=8, default="1"),
            Field(start=9, end=9, value="E"),
            # another fields that must not be counted
            Field(start=8, end=8, default="2"),
            Field(start=9, end=9, value="T"),
        ]

        expected_value = 2
        result = count_cnab_lines_1_E(fields)

        self.assertEqual(expected_value, result)
