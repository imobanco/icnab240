import unittest

from pyCNAB240.core import Field
from pyCNAB240.pipe_and_filter.check import check_missing_given_data_identifiers


class CheckMissingGivenDataIdentifiersTestCase(unittest.TestCase):
    def test_check_missing_given_data_identifiers(self):
        fields = [
            Field(identifier="a"),
            Field(identifier="b", default=0),
            Field(identifier="c", default="Brancos"),
            Field(identifier="d", reasonable_default="Calculavél"),
            Field(identifier="e", reasonable_default="Vazio"),
            Field(identifier="f", reasonable_default=1600),
            Field(identifier="g", default=123, reasonable_default="Calculavél"),
            Field(identifier="h", default=""),
            Field(identifier="i"),
        ]

        # se fields tiver com todos os reasonable_default não precisa do patterns
        patterns = ("a", "b", "c", "d", "e", "f", "g")
        data = {"b": 1}

        with self.assertRaises(ValueError):
            check_missing_given_data_identifiers(fields, patterns, data)
