import unittest

from pyCNAB240.core import Field, main_fields
from pyCNAB240.pipe_and_filter.set import set_insert_segments


class SetInsertSegmentsTestCase(unittest.TestCase):
    def test_insert_segments_no_change(self):
        fields = [Field(identifier="a"), Field(identifier="b"), Field(identifier="c")]

        fields_result = set_insert_segments(fields, 1, "b", None)

        self.assertEqual(fields, fields_result)

    def test_insert_segments_only_one(self):
        fields = [Field(identifier="a"), Field(identifier="b"), Field(identifier="c")]

        patterns = "b"

        expected = [
            Field(identifier="a"),
            Field(identifier="b"),
            Field(identifier="b"),
            Field(identifier="c"),
        ]

        result = set_insert_segments(fields, 2, "b", patterns)
        self.assertEqual(expected, result)

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

        result = set_insert_segments(fields, 3, "b", patterns)
        self.assertEqual(expected, result)

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

        result = set_insert_segments(fields, 2, "d", patterns)
        self.assertEqual(expected, result)

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

        result = set_insert_segments(fields, 4, "d", patterns)
        self.assertEqual(expected, result)

    def test_set_data_to_fields(self):
        fields = [
            Field(identifier="a"),
            Field(identifier="b"),
            Field(identifier="b"),
            Field(identifier="b"),
            Field(identifier="c"),
            Field(identifier="c"),
            Field(identifier="c"),
            Field(identifier="d"),
        ]
        # TODO: checar porque o valor esta sendo transformado em string no processo
        data = {"b": ["1", "2", "3"], "c": ["X", "Y", "Z"]}

        expected = [
            Field(identifier="a"),
            Field(identifier="b", value=1),
            Field(identifier="b", value=2),
            Field(identifier="b", value=3),
            Field(identifier="c", value="X"),
            Field(identifier="c", value="Y"),
            Field(identifier="c", value="Z"),
            Field(identifier="d"),
        ]

        result = set_data_to_fields(fields, data)
        self.assertEqual(expected, result)
