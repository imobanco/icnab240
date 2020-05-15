import unittest

from pyCNAB240.core import Field
from pyCNAB240.pipe_and_filter.set import set_data_to_fields


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

        for index, field in enumerate(fields):
            with self.subTest(index):
                expec = expected[index]

                set_data_to_fields([field], data)
                self.assertEqual(
                    [expec],
                    [field],
                    msg=f"O valor esperado é diferente! {expec.value} != {field.value}",
                )
