import unittest

from icnab240.core import Field
from icnab240.pipe_and_filter.count import count_cnab_lines_1


class CNABTestCase(unittest.TestCase):
    def test_count_cnab_lines_1(self):

        fields = [
            Field(start=8, end=8, default="1"),
            # another fields that must not be counted
            Field(start=8, end=8, default="0"),
            Field(start=8, end=8, value="2"),
            Field(start=8, end=8, value="3"),
            Field(start=8, end=8, value="4"),
            Field(start=8, end=8, value="5"),
            Field(start=8, end=8, value="9"),
        ]

        expected_value = 1
        result = count_cnab_lines_1(fields)

        self.assertEqual(expected_value, result)
