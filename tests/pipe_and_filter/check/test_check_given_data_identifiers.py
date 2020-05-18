import unittest

from icnab240.core import Field
from icnab240.pipe_and_filter.check import check_given_data_identifiers


class CheckOverwritingDataTestCase(unittest.TestCase):
    def test_check_given_data_identifiers(self):
        fields = [Field(identifier="a")]
        patterns = ("a",)
        data = {"b": ["1"]}
        with self.assertRaises(ValueError):
            check_given_data_identifiers(fields, patterns, data)
