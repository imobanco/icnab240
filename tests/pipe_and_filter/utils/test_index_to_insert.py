import unittest

from pyCNAB240.core import Field
from pyCNAB240.pipe_and_filter.utils import index_to_insert


class IndexToInsertTestCase(unittest.TestCase):
    def test_index_to_insert(self):

        fields = [
            Field(identifier="a"),
            Field(identifier="b"),
            Field(identifier="c"),
            Field(identifier="d"),
        ]
        expected_value = 3
        result = index_to_insert(fields, "c")
        self.assertEqual(expected_value, result)
