import unittest

from pyCNAB240.core import Field, main_fields
from pyCNAB240.pipe_and_filter import *


class CNABTestCase(unittest.TestCase):
    def test_insert_segments_no_change(self):
        fields = [Field(identifier="a"), Field(identifier="b"), Field(identifier="c")]

        fields_result = insert_segments(fields, 1, "b", None)

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

        result = insert_segments(fields, 2, "b", patterns)
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

        result = insert_segments(fields, 3, "b", patterns)
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

        result = insert_segments(fields, 2, "d", patterns)
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

        result = insert_segments(fields, 4, "d", patterns)
        self.assertEqual(expected, result)

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

    def test_extract_identifiers_that_have_default_or_reasonable_default(self):
        fields = [
            Field(identifier="a"),
            Field(identifier="b", default=0),
            Field(identifier="c", default="Brancos"),
            Field(identifier="d", reasonable_default="Calculavél"),
            Field(identifier="e", reasonable_default="Vazio"),
            Field(identifier="f", reasonable_default=1600),
            Field(identifier="g", default=123, reasonable_default="Calculavél"),
            Field(identifier="h"),
        ]

        expected = set(["b", "c", "d", "e", "f", "g"])

        result = extract_identifiers_that_have_default_or_reasonable_default(fields)
        self.assertEqual(expected, result)

    def test_extract_identifiers_default_or_reasonable_default_empty(self):
        """
        Note: quando se lê de um arquivo .csv se o valor do campo não existir
              não vem com None, mas sim com ''. Como a criação da dataclass
              força que caso não seja passado um valor para um do atributos
              este será None, e não ''.
        """
        fields = [
            Field(identifier="a"),
            Field(identifier="b", default=""),
            Field(identifier="c", default=0),
            Field(identifier="d", default="Brancos"),
            Field(identifier="e", reasonable_default=""),
            Field(identifier="f", reasonable_default="Calculavél"),
            Field(identifier="g", reasonable_default="Vazio"),
            Field(identifier="h", reasonable_default=1600),
            Field(identifier="i", default=123, reasonable_default="Calculavél"),
            Field(identifier="j", default="", reasonable_default=""),
            Field(identifier="l"),
        ]

        expected = set(["c", "d", "f", "g", "i", "h"])

        result = extract_identifiers_that_have_default_or_reasonable_default(fields)
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

    def test_check_overwriting_data_minimal(self):
        fields = [Field(identifier="a", reasonable_default="123")]

        data = {"a": ["1"]}

        with self.assertRaises(ValueError):
            check_overwriting_data(fields, data)

    def test_check_overwriting_data(self):
        fields = [
            Field(identifier="a", reasonable_default="123"),
            Field(identifier="b"),
        ]

        data = {"a": ["1"]}

        with self.assertRaises(ValueError):
            check_overwriting_data(fields, data)

    def test_check_given_data_identifiers(self):
        fields = [Field(identifier="a")]
        patterns = ("a",)
        data = {"b": ["1"]}
        with self.assertRaises(ValueError):
            check_given_data_identifiers(fields, patterns, data)

    def test_check_none_value(self):
        fields = [Field()]
        with self.assertRaises(ValueError):
            check_none_value(fields)

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
