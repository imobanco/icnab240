from ...utils import MockedFillerTestCase

from icnab240 import Field
from icnab240.pipe_and_filter.set import set_default_value


class SetDefaultValueTestCase(MockedFillerTestCase):
    def test_alfa(self):
        """
        Dado uma lista que tem o campo `num_or_str` igual a Alfa que não tenha `default` igual a "Brancos" ou "Vazio"
        Quando eu setar o valor default
        Então o valor não é alterado
        """
        field = Field(num_or_str="Alfa", value="original")

        self.assertEqual("original", field.value)

        set_default_value([field])

        self.assertEqual("original", field.value)

    def test_alfa_brancos(self):
        """
        Dado uma lista que tem o campo `num_or_str` igual a Alfa que tenha `default` igual a "Brancos"
        Quando eu setar o valor default
        Então o valor é alterado para o valor de preenchimento
        """
        field = Field(num_or_str="Alfa", default="Brancos", value="original")

        self.assertEqual("original", field.value)

        set_default_value([field])

        self.assertEqual(self.fill_value, field.value)

    def test_alfa_vazio(self):
        """
        Dado uma lista que tem o campo `num_or_str` igual Alfa que tenha `default` "Vazio"
        Quando eu setar o valor default
        Então o valor é alterado para o valor de preenchimento
        """
        field = Field(num_or_str="Alfa", reasonable_default="Vazio", value="original")

        self.assertEqual("original", field.value)

        set_default_value([field])

        self.assertEqual(self.fill_value, field.value)

    def test_num(self):
        """
        Dado uma lista de campo Num que não tenha `reasonable_default` "Vazio"
        Quando eu setar o valor default
        Então o valor não é alterado
        """
        field = Field(num_or_str="Num", value="original")

        self.assertEqual("original", field.value)

        set_default_value([field])

        self.assertEqual("original", field.value)

    def test_num_vazio(self):
        """
        Dado uma lista de campo Num que tenha `reasonable_default` "Vazio"
        Quando eu setar o valor default
        Então o valor é alterado '0' (preenchimento numérico)
        """
        field = Field(num_or_str="Num", reasonable_default="Vazio", value="original")

        self.assertEqual("original", field.value)

        set_default_value([field])

        self.assertEqual("0", field.value)

    def test_default(self):
        """
        Dado uma lista de campo que tenha `default` que não seja `None` ou `''` ou 'Brancos'
        Quando eu setar o valor default
        Então o valor é alterado para o `default`
        """
        field = Field(default="foo", value="original")

        self.assertEqual("original", field.value)

        set_default_value([field])

        self.assertEqual("foo", field.value)

    def test_default_empty(self):
        """
        Dado uma lista de campo que tenha `default` que seja `''`
        Quando eu setar o valor default
        Então o valor não é alterado
        """
        field = Field(default="", value="original")

        self.assertEqual("original", field.value)

        set_default_value([field])

        self.assertEqual("original", field.value)

    def test_default_none(self):
        """
        Dado uma lista de campo que tenha `default` que seja `None`
        Quando eu setar o valor default
        Então o valor não é alterado
        """
        field = Field(default=None, value="original")

        self.assertEqual("original", field.value)

        set_default_value([field])

        self.assertEqual("original", field.value)

    def test_default_brancos(self):
        """
        Dado uma lista de campo que tenha `default` que seja 'Brancos'
        Quando eu setar o valor default
        Então o valor não é alterado
        """
        field = Field(default="Brancos", value="original")

        self.assertEqual("original", field.value)

        set_default_value([field])

        self.assertEqual("original", field.value)

    def test_reasonable_default(self):
        """
        Dado uma lista de campo que tenha `reasonable_default` que não seja `None` ou `''` ou 'Calculável'
        Quando eu setar o valor default
        Então o valor é alterado para o `reasonable_default`
        """
        field = Field(reasonable_default="foo", value="original")

        self.assertEqual("original", field.value)

        set_default_value([field])

        self.assertEqual("foo", field.value)

    def test_reasonable_default_empty(self):
        """
        Dado uma lista de campo que tenha `reasonable_default` que seja `''`
        Quando eu setar o valor default
        Então o valor não é alterado
        """
        field = Field(reasonable_default="", value="original")

        self.assertEqual("original", field.value)

        set_default_value([field])

        self.assertEqual("original", field.value)

    def test_reasonable_default_none(self):
        """
        Dado uma lista de campo que tenha `reasonable_default` que seja `None`
        Quando eu setar o valor default
        Então o valor não é alterado
        """
        field = Field(reasonable_default=None, value="original")

        self.assertEqual("original", field.value)

        set_default_value([field])

        self.assertEqual("original", field.value)

    def test_reasonable_default_calculavel(self):
        """
        Dado uma lista de campo que tenha `reasonable_default` que seja 'Calculável'
        Quando eu setar o valor default
        Então o valor não é alterado
        """
        field = Field(reasonable_default="Calculável", value="original")

        self.assertEqual("original", field.value)

        set_default_value([field])

        self.assertEqual("original", field.value)
