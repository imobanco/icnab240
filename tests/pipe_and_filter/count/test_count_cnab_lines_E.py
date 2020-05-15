import unittest

from icnab240.core import Field
from icnab240.pipe_and_filter.count import count_cnab_lines_E


class CNABTestCase(unittest.TestCase):
    def test_count_cnab_lines_E(self):

        fields = [
            Field(start=9, end=9, value="E"),
            Field(start=9, end=9, value="E"),
            # another fields that must not be counted
            Field(start=9, end=9, value="R"),
            Field(start=9, end=9, value="T"),
            Field(start=8, end=8, value="E"),
        ]

        expected_value = 2
        result = count_cnab_lines_E(fields)

        self.assertEqual(expected_value, result)
