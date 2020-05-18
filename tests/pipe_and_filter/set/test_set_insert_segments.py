import unittest

from icnab240.core import Field
from icnab240.pipe_and_filter.set import set_insert_segments


class SetInsertSegmentsTestCase(unittest.TestCase):
    def test_insert_segments_no_change(self):
        fields = [Field(identifier="a"), Field(identifier="b"), Field(identifier="c")]

        expected = [Field(identifier="a"), Field(identifier="b"), Field(identifier="c")]

        set_insert_segments(fields, 1, "b", None)

        self.assertEqual(expected, fields)

    def test_insert_segments_only_one(self):
        fields = [Field(identifier="a"), Field(identifier="b"), Field(identifier="c")]

        patterns = "b"

        expected = [
            Field(identifier="a"),
            Field(identifier="b"),
            Field(identifier="b"),
            Field(identifier="c"),
        ]

        set_insert_segments(fields, 2, "b", patterns)
        self.assertEqual(expected, fields)

    def test_insert_segments_only_two(self):
        fields = [Field(identifier="a"), Field(identifier="b"), Field(identifier="c")]

        patterns = "b"

        expected = [
            Field(identifier="a"),
            Field(identifier="b"),
            Field(identifier="b"),
            Field(identifier="b"),
            Field(identifier="c"),
        ]

        set_insert_segments(fields, 3, "b", patterns)
        self.assertEqual(expected, fields)

    def test_insert_segments_more_than_one_pattern(self):
        fields = [
            Field(identifier="a"),
            Field(identifier="b"),
            Field(identifier="c"),
            Field(identifier="d"),
            Field(identifier="e"),
            Field(identifier="f"),
        ]

        patterns = ("b", "c")

        expected = [
            Field(identifier="a"),
            Field(identifier="b"),
            Field(identifier="c"),
            Field(identifier="d"),
            Field(identifier="b"),
            Field(identifier="c"),
            Field(identifier="e"),
            Field(identifier="f"),
        ]

        set_insert_segments(fields, 2, "d", patterns)
        self.assertEqual(expected, fields)

    def test_insert_segments_realistic(self):
        fields = [
            Field(identifier="a"),
            Field(identifier="b"),
            Field(identifier="c"),
            Field(identifier="d"),
            Field(identifier="e"),
            Field(identifier="f"),
        ]

        patterns = ("b", "c", "d")

        expected = [
            Field(identifier="a"),
            Field(identifier="b"),
            Field(identifier="c"),
            Field(identifier="d"),
            Field(identifier="b"),
            Field(identifier="c"),
            Field(identifier="d"),
            Field(identifier="b"),
            Field(identifier="c"),
            Field(identifier="d"),
            Field(identifier="b"),
            Field(identifier="c"),
            Field(identifier="d"),
            Field(identifier="e"),
            Field(identifier="f"),
        ]

        set_insert_segments(fields, 4, "d", patterns)
        self.assertEqual(expected, fields)
