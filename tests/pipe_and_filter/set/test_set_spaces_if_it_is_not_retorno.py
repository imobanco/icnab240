from ...utils import MockedFillerTestCase

from icnab240 import Field
from icnab240.pipe_and_filter.set import set_spaces_if_it_is_not_retorno


class SetSpacesIfItIsNotRetornoTestCase(MockedFillerTestCase):
    def test_not_5(self):
        field = Field(start=40, end=44, value=1, length=4, identifier=".")

        self.assertIsNone(field.value_to_cnab)

        set_spaces_if_it_is_not_retorno([field])

        self.assertIsNone(field.value_to_cnab)

    def test_5(self):
        field = Field(start=40, end=44, value=1, length=4, identifier=".5")

        self.assertIsNone(field.value_to_cnab)

        set_spaces_if_it_is_not_retorno([field])

        self.assertEqual("####", field.value_to_cnab)
        self.assertEqual("####", field.value)

    def test_23(self):
        field = Field(start=23, end=44, value=1, length=4, identifier=".5")

        self.assertIsNone(field.value_to_cnab)

        set_spaces_if_it_is_not_retorno([field])

        self.assertIsNone(field.value_to_cnab)
        self.assertEqual('1', field.value)

    def test_24(self):
        field = Field(start=24, end=44, value=1, length=4, identifier=".5")

        self.assertIsNone(field.value_to_cnab)

        set_spaces_if_it_is_not_retorno([field])

        self.assertEqual("####", field.value_to_cnab)
        self.assertEqual("####", field.value)

    def test_116(self):
        field = Field(start=116, end=44, value=1, length=4, identifier=".5")

        self.assertIsNone(field.value_to_cnab)

        set_spaces_if_it_is_not_retorno([field])

        self.assertEqual("####", field.value_to_cnab)
        self.assertEqual("####", field.value)

    def test_117(self):
        field = Field(start=117, end=44, value=1, length=4, identifier=".5")

        self.assertIsNone(field.value_to_cnab)

        set_spaces_if_it_is_not_retorno([field])

        self.assertIsNone(field.value_to_cnab)
        self.assertEqual('1', field.value)
