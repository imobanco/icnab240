import unittest

from icnab240.core import Field
from icnab240.pipe_and_filter.check import check_overwriting_data


class CheckOverwritingDataTestCase(unittest.TestCase):
    def test_check_overwriting_data_minimal(self):
        fields = [Field(identifier="a", reasonable_default="123")]

        data = {"a": ["1"]}

        with self.assertRaises(ValueError):
            check_overwriting_data(fields, data)

    def test_check_overwriting_data(self):
        fields = [
            Field(identifier="a", reasonable_default="123"),
            Field(identifier="b"),
        ]

        data = {"a": ["1"]}

        with self.assertRaises(ValueError):
            check_overwriting_data(fields, data)
