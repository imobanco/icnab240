from unittest import TestCase

from pyCNAB240.pipe_and_filter.check import check_input_data_type


class CheckValueTypeTestCase(TestCase):
    def test_str(self):
        self.assertIsNone(check_input_data_type({"foo": "bar"}))

    def test_list(self):
        self.assertIsNone(check_input_data_type({"foo": ["bar"]}))

    def test_others(self):
        other_values = [
            "",
            1,
            [],
            {},
            set(),
            (),
            1.0,
            [""],
            [1],
            [[]],
            [{}],
            [set()],
            [()],
            [1.0],
        ]
        for value in other_values:
            with self.subTest(f"valor:{value}"):
                self.assertRaises(TypeError, check_input_data_type, {"foo": value})
