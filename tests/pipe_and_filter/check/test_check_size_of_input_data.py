import unittest

from icnab240.core import Field
from icnab240.pipe_and_filter.check import check_size_of_input_data


class CheckSizeOfInputDataTestCase(unittest.TestCase):
    def test_check_size_of_input_data_minimal(self):
        fields = [Field(identifier="a", length=1)]

        data = {"a": ["longer"]}

        with self.assertRaises(ValueError):
            check_size_of_input_data(fields, data)

    def test_check_size_of_input_data_num_decimals(self):
        fields = [Field(identifier="a", length=1, num_decimals="2")]

        data = {"a": ["xyzw"]}

        with self.assertRaises(ValueError):
            check_size_of_input_data(fields, data)

    def test_check_size_of_input_data_more_than_one_field(self):
        fields = [
            Field(identifier="a", length=1, num_decimals=""),
            Field(identifier="b", length=1, num_decimals="2"),
        ]

        data = {"b": ["xyzw"]}

        with self.assertRaises(ValueError):
            check_size_of_input_data(fields, data)
