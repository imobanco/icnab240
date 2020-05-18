import unittest

from icnab240.pipe_and_filter.build import build_cnab_lines


class CNABTestCase(unittest.TestCase):
    def test_build_cnab_lines(self):
        pieces = ["A", "B\n", "C\n"]

        expected_value = ["AB\n", "C\n"]
        result = build_cnab_lines(pieces)

        self.assertEqual(expected_value, result)
