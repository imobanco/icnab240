import unittest

from icnab240.core import Field
from icnab240.pipe_and_filter.utils import inscription_type


class InscriptionTypeTestCase(unittest.TestCase):
    def test_inscription_type_cpf(self):
        cpf = "00140154558"
        expected_value = 1
        result = inscription_type(cpf)

        self.assertEqual(expected_value, result)

    def test_inscription_type_cnpj(self):
        cnpj = "00002238490226"
        expected_value = 2
        result = inscription_type(cnpj)

        self.assertEqual(expected_value, result)

    def test_inscription_type_not_cpf_or_cnpj_raise(self):
        with self.assertRaises(ValueError):
            inscription_type(None)
