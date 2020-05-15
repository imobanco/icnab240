from unittest import TestCase

from icnab240.pipe_and_filter.build import build_main_fields


class BuildMainFieldsTestCase(TestCase):
    def setUp(self):
        self.main_fields = build_main_fields()

    def test_len(self):
        self.assertEqual(len(self.main_fields), 229)

    def test_end_start(self):
        for field in self.main_fields:
            with self.subTest(field):
                self.assertIsInstance(field.start, int)
                self.assertIsInstance(field.end, int)
