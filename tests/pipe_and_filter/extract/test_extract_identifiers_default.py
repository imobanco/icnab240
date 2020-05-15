import unittest

from icnab240.core import Field
from icnab240.pipe_and_filter.extract import extract_identifiers_default


class ExtractIdentifiersDefaultTestCase(unittest.TestCase):
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

        result = extract_identifiers_default(fields)
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

        result = extract_identifiers_default(fields)
        self.assertEqual(expected, result)
