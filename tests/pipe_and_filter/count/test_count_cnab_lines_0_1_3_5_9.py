import unittest

from icnab240.core import Field
from icnab240.pipe_and_filter.count import count_cnab_lines_0_1_3_5_9


class CNABTestCase(unittest.TestCase):
    def test_count_cnab_lines_0_1_3_5_9(self):
        fields = [
            Field(start=8, end=8),
            Field(start=8, end=8),
            Field(start=8, end=8),
            Field(start=8, end=8),
            Field(start=8, end=5),
            Field(start=4, end=8),
        ]

        expected_value = 4
        result = count_cnab_lines_0_1_3_5_9(fields)

        self.assertEqual(expected_value, result)
