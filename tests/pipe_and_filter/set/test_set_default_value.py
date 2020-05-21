from ...utils import MockedFillerTestCase

from icnab240 import Field
from icnab240.pipe_and_filter.set import set_default_value


class SetDefaultValueTestCase(MockedFillerTestCase):
    def test_alfa(self):
        """
        Dado uma lista de Fields que tem o campo `num_or_str` igual a Alfa que não tenha `default` igual a "Brancos" ou "Vazio"
        Quando eu setar o valor default
        Então o valor não é alterado
        """
        field = Field(num_or_str="Alfa", value="original")

        self.assertEqual("original", field.value)

        set_default_value([field])

        self.assertEqual("original", field.value)

    def test_alfa_brancos(self):
        """
        Dado uma lista de Fields que tem o campo `num_or_str` igual a "Alfa" e que tenha `default` igual a "Brancos"
        Quando eu setar o valor default
        Então o valor é alterado para o valor de preenchimento
        """
        field = Field(num_or_str="Alfa", default="Brancos", value="original")

        self.assertEqual("original", field.value)

        set_default_value([field])

        self.assertEqual(self.fill_value, field.value)

    def test_alfa_vazio(self):
        """
        Dado uma lista de Fields que tem o campo `num_or_str` igual a "Alfa" e que tenha `default` "Vazio"
        Quando eu setar o valor default
        Então o valor é alterado para o valor de preenchimento
        """
        field = Field(num_or_str="Alfa", reasonable_default="Vazio", value="original")

        self.assertEqual("original", field.value)

        set_default_value([field])

        self.assertEqual(self.fill_value, field.value)

    def test_num(self):
        """
        Dado uma lista de Fields que tenha o campo `num_or_str` igual a Num e que não tenha `reasonable_default` "Vazio"
        Quando eu setar o valor default
        Então o valor não é alterado
        """
        field = Field(num_or_str="Num", value="original")

        self.assertEqual("original", field.value)

        set_default_value([field])

        self.assertEqual("original", field.value)

    def test_num_vazio(self):
        """
        Dado uma lista de Fields que tenha o campo `num_or_str` igual a Num que tenha `reasonable_default` "Vazio"
        Quando eu setar o valor default
        Então o valor é alterado '0' (preenchimento numérico)
        """
        field = Field(num_or_str="Num", reasonable_default="Vazio", value="original")

        self.assertEqual("original", field.value)

        set_default_value([field])

        self.assertEqual("0", field.value)

    def test_default(self):
        """
        Dado uma lista de Fields que tenha campo `default` não igual a `None` ou `''` ou 'Brancos'
        Quando eu setar o valor default
        Então o valor é alterado para o `default`
        """
        field = Field(default="foo", value="original")

        self.assertEqual("original", field.value)

        set_default_value([field])

        self.assertEqual("foo", field.value)

    def test_default_empty(self):
        """
        Dado uma lista de Fields que tenha campo `default` igual a `''`
        Quando eu setar o valor default
        Então o valor não é alterado
        """
        field = Field(default="", value="original")

        self.assertEqual("original", field.value)

        set_default_value([field])

        self.assertEqual("original", field.value)

    def test_default_none(self):
        """
        Dado uma lista de Fields que tenha campo `default` igual a `None`
        Quando eu setar o valor default
        Então o valor não é alterado
        """
        field = Field(default=None, value="original")

        self.assertEqual("original", field.value)

        set_default_value([field])

        self.assertEqual("original", field.value)

    def test_default_brancos(self):
        """
        Dado uma lista de Fields que tenha campo `default` igual a 'Brancos'
        Quando eu setar o valor default
        Então o valor não é alterado
        """
        field = Field(default="Brancos", value="original")

        self.assertEqual("original", field.value)

        set_default_value([field])

        self.assertEqual("original", field.value)

    def test_reasonable_default(self):
        """
        Dado uma lista de Fields que tena o campo `reasonable_default` que não igual a `None` ou `''` ou 'Calculável'
        Quando eu setar o valor default
        Então o valor é alterado para o `reasonable_default`
        """
        field = Field(reasonable_default="foo", value="original")

        self.assertEqual("original", field.value)

        set_default_value([field])

        self.assertEqual("foo", field.value)

    def test_reasonable_default_empty(self):
        """
        Dado uma lista de Fields que tena o campo `reasonable_default` que igual a `''`
        Quando eu setar o valor default
        Então o valor não é alterado
        """
        field = Field(reasonable_default="", value="original")

        self.assertEqual("original", field.value)

        set_default_value([field])

        self.assertEqual("original", field.value)

    def test_reasonable_default_none(self):
        """
        Dado uma lista de Fields que tena o campo `reasonable_default` que igual a `None`
        Quando eu setar o valor default
        Então o valor não é alterado
        """
        field = Field(reasonable_default=None, value="original")

        self.assertEqual("original", field.value)

        set_default_value([field])

        self.assertEqual("original", field.value)

    def test_reasonable_default_calculavel(self):
        """
        Dado uma lista de Fields que tena o campo `reasonable_default` que igual a 'Calculável'
        Quando eu setar o valor default
        Então o valor não é alterado
        """
        field = Field(reasonable_default="Calculável", value="original")

        self.assertEqual("original", field.value)

        set_default_value([field])

        self.assertEqual("original", field.value)
