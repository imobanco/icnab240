import unittest

from pyCNAB240.core import Field
from pyCNAB240.pipe_and_filter.check import check_start_and_end


class CheckStartAndEndTestCase(unittest.TestCase):
    def test_check_start_and_end_not_raises(self):
        fields = [Field(start=1, end=3), Field(start=4, end=10)]

        check_start_and_end(fields)

    def test_check_start_and_end_raises(self):
        fields = [Field(start=1, end=3), Field(start=5, end=10)]
        with self.assertRaises(ValueError):
            check_start_and_end(fields)

    def test_check_start_and_end_end_eq_240(self):
        fields = [
            Field(start=1, end=240),
            Field(start=1, end=3),
            Field(start=4, end=100),
        ]

        check_start_and_end(fields)
