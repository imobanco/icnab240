import unittest

from icnab240.pipe_and_filter.utils import is_value_empty


class IsValueEmptyTestCase(unittest.TestCase):
    def test_empty(self):
        """
        Dado o valor ''
        Quando eu verificar se esse valor é vazio
        Então deve retornar verdadeiro
        """
        self.assertTrue(is_value_empty(""))

    def test_none(self):
        """
        Dado o valor None
        Quando eu verificar se esse valor é vazio
        Então deve retornar verdadeiro
        """
        self.assertTrue(is_value_empty(None))

    def test_others(self):
        """
        Dado qualquer valor diferente de '' e None
        Quando eu verificar se esse valor é vazio
        Então deve retornar falso
        """
        other_values = ["a", 1, 0, -1, [], {}, set()]
        for value in other_values:
            with self.subTest(value):
                self.assertFalse(is_value_empty(value))
