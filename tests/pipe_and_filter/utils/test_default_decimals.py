import unittest

from pyCNAB240.core import Field
from pyCNAB240.pipe_and_filter.utils import default_decimals


class DefaultDecimalsTestCase(unittest.TestCase):
    def test_default_decimals_empty(self):

        field = Field(num_decimals="")

        expected_value = 0
        result = default_decimals(field)

        self.assertEqual(expected_value, result)

    def test_default_decimals_2(self):

        field = Field(num_decimals="2")

        expected_value = 2
        result = default_decimals(field)

        self.assertEqual(expected_value, result)

    def test_default_decimals_2(self):

        field = Field(num_decimals="2/5")

        expected_value = 2
        result = default_decimals(field)

        self.assertEqual(expected_value, result)
