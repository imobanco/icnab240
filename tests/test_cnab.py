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




if __name__ == '__main__':
    unittest.main()