from unittest import TestCase

from pyCNAB240.constants import MAIN_FIELDS


class MainFieldsTestCase(TestCase):
    def test_len(self):
        self.assertEqual(len(MAIN_FIELDS), 229)

    def test_end_start(self):
        for field in MAIN_FIELDS:
            with self.subTest(field):
                self.assertIsInstance(field.start, int)
                self.assertIsInstance(field.end, int)
