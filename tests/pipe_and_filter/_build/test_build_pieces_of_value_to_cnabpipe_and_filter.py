import unittest

from pyCNAB240.core import Field
from pyCNAB240.pipe_and_filter.build import build_pieces_of_value_to_cnab


class BuildPiecesOfValueToCNABTestCase(unittest.TestCase):
    def test_build_pieces_of_value_to_cnab(self):
        fields = [
            Field(value_to_cnab="A", end=10),
            Field(value_to_cnab="B", end=240),
            Field(value_to_cnab="C", end=1),
        ]

        expected_value = ["A", "B\n", "C"]
        result = build_pieces_of_value_to_cnab(fields)

        self.assertEqual(expected_value, result)
