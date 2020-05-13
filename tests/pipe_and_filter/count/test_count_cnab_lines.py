import unittest

from pyCNAB240.core import Field
from pyCNAB240.pipe_and_filter.count import count_cnab_lines


class CNABTestCase(unittest.TestCase):
    def test_count_cnab_lines(self):
        fields = [Field(end=240), Field(end=100), Field(end=240), Field(end=123)]

        expected_value = 2
        result = count_cnab_lines(fields)

        self.assertEqual(expected_value, result)
