import unittest

from icnab240.pipe_and_filter.check import check_lines_length


class CheckNoneValueTestCase(unittest.TestCase):
    def test_check_lines_length_line_bigger(self):
        lines = ["a ling line\n"]
        wrong_length = 3
        with self.assertRaises(ValueError):
            check_lines_length(lines, wrong_length)

    def test_check_lines_length_line_smaller(self):
        lines = ["a ling line\n"]
        wrong_length = 10
        with self.assertRaises(ValueError):
            check_lines_length(lines, wrong_length)
