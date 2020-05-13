import unittest

from pyCNAB240.core import Field
from pyCNAB240.pipe_and_filter.utils import compose


class ComposeTestCase(unittest.TestCase):
    def test_compose(self):
        def add_double(x, y):
            return x + y ** 2

        def add_triple(x, y):
            return x + 3 * y

        x = 1
        y = 2

        f = compose((add_double, y), (add_triple, y))

        expected_value = add_double(add_triple(x, y), y)
        result = f(x)

        self.assertEqual(expected_value, result)
