from unittest import TestCase
from unittest.mock import patch, MagicMock, mock_open, call

from icnab240.controllers.file import write_cnab, _write_cnab


class FileTestCase(TestCase):
    def test__write_cnab(self):
        name = "teste"
        lines = ["a", "b", "c"]

        mocked_file = mock_open()
        with patch(
            "icnab240.controllers.file.open", mocked_file, create=True
        ) as mocked_file:

            _write_cnab(name, lines)

            write = mocked_file.return_value.write
            self.assertIsInstance(write, MagicMock)
            self.assertEqual(write.call_count, 3)
            write.assert_has_calls([call("a"), call("b"), call("c")])

    def test_write_cnab(self):
        name = "teste"
        fields = ["a", "b", "c"]

        with patch(
            "icnab240.controllers.file.build_pieces_of_value_to_cnab",
            return_value="pieces",
        ) as mocked_pieces, patch(
            "icnab240.controllers.file.build_cnab_lines", return_value="lines"
        ) as mocked_lines, patch(
            "icnab240.controllers.file._write_cnab"
        ) as mocked__write:

            write_cnab(name, fields)

            self.assertIsInstance(mocked_pieces, MagicMock)
            mocked_pieces.assert_called_once_with(fields)

            self.assertIsInstance(mocked_lines, MagicMock)
            mocked_lines.assert_called_once_with(mocked_pieces.return_value)

            self.assertIsInstance(mocked__write, MagicMock)
            mocked__write.assert_called_once_with(name, mocked_lines.return_value)
