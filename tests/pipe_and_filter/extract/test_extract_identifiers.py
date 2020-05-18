import unittest

from icnab240.core import Field
from icnab240.pipe_and_filter.extract import extract_identifiers


class ExtractIdentifiersTestCase(unittest.TestCase):
    def test_extract_identifiers(self):
        fields = [
            Field(identifier="a"),
            Field(identifier="b"),
            Field(identifier="c"),
            Field(identifier="d"),
            Field(identifier="e"),
            Field(identifier="f"),
        ]

        patterns = ("a", "b", "c")

        expected = set(["a", "b", "c"])

        result = extract_identifiers(fields, patterns)
        self.assertEqual(expected, result)
