import unittest

from icnab240.core import Field
from icnab240.pipe_and_filter.check import check_none_value


class CheckNoneValueTestCase(unittest.TestCase):
    def test_check_none_value(self):
        fields = [Field()]
        with self.assertRaises(ValueError):
            check_none_value(fields)
