from ...utils import MockedFillerTestCase

from icnab240 import Field
from icnab240.pipe_and_filter.set import set_fill_value_to_cnab


class SetFillValueToCnabTestCase(MockedFillerTestCase):
    def test_num(self):
        field = Field(value=1, length=2, num_or_str="Num")

        self.assertIsNone(field.value_to_cnab)

        set_fill_value_to_cnab([field])

        self.assertEqual("01", field.value_to_cnab)

    def test_str(self):
        field = Field(value="1", length=2)

        self.assertIsNone(field.value_to_cnab)

        set_fill_value_to_cnab([field])

        self.assertEqual("#1", field.value_to_cnab)

    def test_length(self):
        field = Field(value="1", length=1)

        self.assertIsNone(field.value_to_cnab)

        set_fill_value_to_cnab([field])

        self.assertEqual("1", field.value_to_cnab)
