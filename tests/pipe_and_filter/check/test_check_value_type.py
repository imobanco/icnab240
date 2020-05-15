from unittest import TestCase

from icnab240.pipe_and_filter.check import check_value_type


class CheckValueTypeTestCase(TestCase):
    def test_str(self):
        self.assertIsNone(check_value_type("foo"))

    def test_others(self):
        other_values = ["", 1, [], {}, set(), (), 1.0, None]
        for value in other_values:
            with self.subTest(f"valor:{value}"):
                self.assertRaises(TypeError, check_value_type, value)
