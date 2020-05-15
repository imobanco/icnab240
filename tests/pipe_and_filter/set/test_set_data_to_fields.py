import unittest

from icnab240.core import Field
from icnab240.pipe_and_filter.set import set_data_to_fields


class SetInsertSegmentsTestCase(unittest.TestCase):
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

        for index, field in enumerate(fields):
            with self.subTest(index):
                expec = expected[index]

                set_data_to_fields([field], data)
                self.assertEqual(
                    [expec],
                    [field],
                    msg=f"O valor esperado é diferente! "
                    f"{type(expec.value)}({expec.value}) != "
                    f"{type(field.value)}({field.value})",
                )
