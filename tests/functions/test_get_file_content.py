from pathlib import Path
import unittest

import sys

from functions.get_file_content import get_file_content
from functions.utils import check_has_at_least
from tempfile import TemporaryDirectory


class TestGetFileContent(unittest.TestCase):
    def test_double_dot(self):
        assert ".. is outside of ." in get_file_content(".", "..")

    def test_double_dot_slash(self):
        assert ".. is outside of ." in get_file_content(".", "../")

    def test_no_read_permission(self):
        with TemporaryDirectory() as tmpdir:
            main_py = Path(f"{tmpdir}/main.py")
            main_py.write_text("Woooooooooooah there buddy")
            main_py.chmod(000)
            assert get_file_content(tmpdir, main_py.as_posix()).startswith(
                "error: no permission for reading file"
            )

    def test_existent_files(self):
        with TemporaryDirectory() as tmpdir:
            main_py = Path(f"{tmpdir}/main.py")
            main_py.write_text("this is the main :D")

            text = get_file_content(tmpdir, str(main_py))

            assert text == "this is the main :D"

    def test_with_directory(self):
        with TemporaryDirectory() as tmpdir:
            test_dir_p = Path(tmpdir / Path("test_dir"))
            test_dir_p.mkdir()
            assert "is not a file" in get_file_content(tmpdir, str(test_dir_p))

    def test_non_existent_file(self):
        assert "error: file calculator/bin/blah/blee/bloo.txt does not exist" in get_file_content(
            "calculator", "./bin/blah/blee/bloo.txt"
        )

    """
        Platform specific tests
    """

    def test_c_drive(self):
        if sys.platform == "win32":
            # TODO test this
            assert "C:\\ is outside of" in get_file_content(".", "C:\\")

    def test_slash_bin(self):
        if sys.platform != "win32":
            assert "error: /bin is outside of calculator" in get_file_content(
                "calculator", "/bin"
            )
