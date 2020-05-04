import unittest

from pyCNAB240.core import Field, main_fields
from pyCNAB240.pipe_and_filter import *


class CNABTestCase(unittest.TestCase):
    def test_check_start_and_end_not_raises(self):
        fields = [Field(start=1, end=3), Field(start=4, end=10)]

        check_start_and_end(fields)

    def test_check_start_and_end_raises(self):
        fields = [Field(start=1, end=3), Field(start=5, end=10)]
        with self.assertRaises(ValueError):
            check_start_and_end(fields)

    def test_check_start_and_end_end_eq_240(self):
        fields = [Field(start=1, end=240),
                  Field(start=1, end=3),
                  Field(start=4, end=100)]

        check_start_and_end(fields)

    def test_build_pieces_of_value_to_cnab(self):
        fields = [Field(value_to_cnab='A', end=10),
                  Field(value_to_cnab='B', end=240),
                  Field(value_to_cnab='C', end=1)]

        expected_value = ['A', 'B\n', 'C']
        result = build_pieces_of_value_to_cnab(fields)

        self.assertEqual(expected_value, result)

    def test_build_cnab_lines(self):
        pieces = ['A', 'B\n', 'C\n']

        expected_value = ['AB\n', 'C\n']
        result = build_cnab_lines(pieces)

        self.assertEqual(expected_value, result)

    def test__write_cnab(self):
        # TODO: How to test this?
        pass

    def test_write_cnab(self):
        # TODO: How to test this?
        pass

    def test_set_bank_number(self):
        fields = [Field(start=1),
                  Field(start=1),
                  Field(start=1)]

        bank_number = 33
        result_fields = set_bank_number(fields, bank_number)
        for field in result_fields:
            self.assertEqual(field.value, bank_number)

    def test_count_cnab_lines(self):
        fields = [Field(end=240), Field(end=100), Field(end=240),
                  Field(end=123)]

        expected_value = 2
        result = count_cnab_lines(fields)

        self.assertEqual(expected_value, result)


    def test_count_cnab_lines_0_1_3_5_9(self):
        fields = [Field(start=8, end=8),
                  Field(start=8, end=8),
                  Field(start=8, end=8),
                  Field(start=8, end=8),
                  Field(start=8, end=5),
                  Field(start=4, end=8)]

        expected_value = 4
        result = count_cnab_lines_0_1_3_5_9(fields)

        self.assertEqual(expected_value, result)



    def test_count_cnab_lines_1_2_3_4_5(self):
        # Note: if default=0 or default=9 it must not be counted
        fields = [Field(start=8, end=8, default=1),
                  Field(start=8, end=8, default=2),
                  Field(start=8, end=8, default=3),
                  Field(start=8, end=8, default=4),
                  Field(start=8, end=8, default=5),
                  Field(start=8, end=8, default=0),
                  Field(start=8, end=8, default=9),
                  ]

        expected_value = 5
        result = count_cnab_lines_1_2_3_4_5(fields)

        self.assertEqual(expected_value, result)

    def test_count_cnab_lines_E(self):

        fields = [Field(start=9, end=9, value='E'),
                  Field(start=9, end=9, value='E'),
                  # another fields that must not be counted
                  Field(start=9, end=9, value='R'),
                  Field(start=9, end=9, value='T'),
                  Field(start=8, end=8, value='E'),
                  ]

        expected_value = 2
        result = count_cnab_lines_E(fields)

        self.assertEqual(expected_value, result)


    def test_count_cnab_lines_1(self):

        fields = [Field(start=8, end=8, default='1'),
                  # another fields that must not be counted
                  Field(start=8, end=8, default='0'),
                  Field(start=8, end=8, value='2'),
                  Field(start=8, end=8, value='3'),
                  Field(start=8, end=8, value='4'),
                  Field(start=8, end=8, value='5'),
                  Field(start=8, end=8, value='9'),
                  ]

        expected_value = 1
        result = count_cnab_lines_1(fields)

        self.assertEqual(expected_value, result)

    def test_count_cnab_lines_1_and_E_type(self):

        fields = [Field(start=8, end=8, default='1'),
                  Field(start=9, end=9, value='E'),
                  # another fields that must not be counted
                  Field(start=8, end=8, default='2'),
                  Field(start=9, end=9, value='T'),
                  ]

        expected_value = 2
        result = count_cnab_lines_1_and_E_type(fields)

        self.assertEqual(expected_value, result)

    def test_default_decimals(self):

        # TODO: after test other functions
        fields = [Field(start=8, end=8, default='1'),
                  Field(start=9, end=9, value='E'),
                  # another fields that must not be counted
                  Field(start=8, end=8, default='2'),
                  Field(start=9, end=9, value='T'),
                  ]

        expected_value = 2
        # Essa função vai deixar de existir
        # ela recebe um objeto field, não uma lista de Fields
        # result = default_decimals(fields)

        # self.assertEqual(expected_value, result)

    def test_compose(self):

        def add_double(x, y):
            return x + y**2

        def add_triple(x, y):
            return x + 3*y

        x = 1
        y = 2

        f = compose((add_double, y), (add_triple, y))

        expected_value = add_double(add_triple(x, y), y)
        result = f(x)

        self.assertEqual(expected_value, result)

    def test_inscription_type_cpf(self):
        cpf = '00140154558'
        expected_value = 1
        result = inscription_type(cpf)

        self.assertEqual(expected_value, result)

    def test_inscription_type_cnpj(self):
        cnpj = '00002238490226'
        expected_value = 2
        result = inscription_type(cnpj)

        self.assertEqual(expected_value, result)

    def test_inscription_type_not_cpf_or_cnpj_raise(self):
        with self.assertRaises(ValueError):
            inscription_type(None)

    def test_index_to_insert(self):

        fields = [Field(identifier='a'), Field(identifier='b'),
                  Field(identifier='c'), Field(identifier='d')]
        expected_value = 3
        result = index_to_insert(fields, 'c')
        self.assertEqual(expected_value, result)

    def test_insert_segments_no_change(self):
        fields = [Field(identifier='a'), Field(identifier='b'),
                  Field(identifier='c')]

        fields_result = insert_segments(fields, 1, 'b', None)

        self.assertEqual(fields, fields_result)

    def test_insert_segments_only_one(self):
        fields = [Field(identifier='a'), Field(identifier='b'),
                  Field(identifier='c')]

        patterns = ('b')

        expected = [Field(identifier='a'), Field(identifier='b'),
                    Field(identifier='b'), Field(identifier='c')]

        result = insert_segments(fields, 2, 'b', patterns)
        self.assertEqual(expected, result)


    def test_insert_segments_only_two(self):
        fields = [Field(identifier='a'), Field(identifier='b'),
                  Field(identifier='c')]

        patterns = ('b')

        expected = [Field(identifier='a'), Field(identifier='b'),
                    Field(identifier='b'), Field(identifier='b'),
                    Field(identifier='c')]

        result = insert_segments(fields, 3, 'b', patterns)
        self.assertEqual(expected, result)

    def test_insert_segments_more_than_one_pattern(self):
        fields = [Field(identifier='a'), Field(identifier='b'),
                  Field(identifier='c'), Field(identifier='d'),
                  Field(identifier='e'), Field(identifier='f'),
                  ]

        patterns = ('b', 'c')

        expected = [Field(identifier='a'), Field(identifier='b'),
                    Field(identifier='c'), Field(identifier='d'),
                    Field(identifier='b'), Field(identifier='c'),
                    Field(identifier='e'), Field(identifier='f')]

        result = insert_segments(fields, 2, 'd', patterns)
        self.assertEqual(expected, result)

    def test_insert_segments_realistic(self):
        fields = [Field(identifier='a'), Field(identifier='b'),
                  Field(identifier='c'), Field(identifier='d'),
                  Field(identifier='e'), Field(identifier='f'),
                  ]

        patterns = ('b', 'c', 'd')

        expected = [Field(identifier='a'),
                    Field(identifier='b'), Field(identifier='c'),
                    Field(identifier='d'),
                    Field(identifier='b'), Field(identifier='c'),
                    Field(identifier='d'),
                    Field(identifier='b'), Field(identifier='c'),
                    Field(identifier='d'),
                    Field(identifier='b'), Field(identifier='c'),
                    Field(identifier='d'),
                    Field(identifier='e'), Field(identifier='f')]

        result = insert_segments(fields, 4, 'd', patterns)
        self.assertEqual(expected, result)

    def test_extract_identifiers(self):
        fields = [Field(identifier='a'), Field(identifier='b'),
                  Field(identifier='c'), Field(identifier='d'),
                  Field(identifier='e'), Field(identifier='f'),
                  ]

        patterns = ('a', 'b', 'c')

        expected = set(['a', 'b', 'c'])

        result = extract_identifiers(fields, patterns)
        self.assertEqual(expected, result)

    def test_extract_identifiers_that_have_default_or_reasonable_default(self):
        fields = [Field(identifier='a'),
                  Field(identifier='b', default=0),
                  Field(identifier='c', default='Brancos'),
                  Field(identifier='d', reasonable_default='Calculavél'),
                  Field(identifier='e', reasonable_default='Vazio'),
                  Field(identifier='f', reasonable_default=1600),
                  Field(identifier='g', default=123, reasonable_default='Calculavél'),
                  Field(identifier='h')
                  ]

        expected = set(['b', 'c', 'd', 'e', 'f', 'g'])

        result = extract_identifiers_that_have_default_or_reasonable_default(fields)
        self.assertEqual(expected, result)

    def test_extract_identifiers_default_or_reasonable_default_empty(self):
        """
        Note: quando se lê de um arquivo .csv se o valor do campo não existir
              não vem com None, mas sim com ''. Como a criação da dataclass
              força que caso não seja passado um valor para um do atributos
              este será None, e não ''.
        """
        fields = [Field(identifier='a'),
                  Field(identifier='b', default=''),
                  Field(identifier='c', default=0),
                  Field(identifier='d', default='Brancos'),
                  Field(identifier='e', reasonable_default=''),
                  Field(identifier='f', reasonable_default='Calculavél'),
                  Field(identifier='g', reasonable_default='Vazio'),
                  Field(identifier='h', reasonable_default=1600),
                  Field(identifier='i', default=123, reasonable_default='Calculavél'),
                  Field(identifier='j', default='', reasonable_default=''),
                  Field(identifier='l')
                  ]

        expected = set(['c', 'd', 'f', 'g', 'i', 'h'])

        result = extract_identifiers_that_have_default_or_reasonable_default(fields)
        self.assertEqual(expected, result)

    def test_get_identifiers_from_input_data(self):
        fields = [Field(identifier='a'),
                  Field(identifier='b', default=0),
                  Field(identifier='c', default='Brancos'),
                  Field(identifier='d', reasonable_default='Calculavél'),
                  Field(identifier='e', reasonable_default='Vazio'),
                  Field(identifier='f', reasonable_default=1600),
                  Field(identifier='g', default=123, reasonable_default='Calculavél'),
                  Field(identifier='h', default=''),
                  Field(identifier='i')
                  ]

        # se fields tiver com todos os reasonable_default não precisa do patterns
        patterns = ('a', 'b', 'c', 'd', 'e', 'f', 'g')
        data = {'b': 1}

        with self.assertRaises(ValueError):
            check_given_data_identifiers(fields, patterns, data)
