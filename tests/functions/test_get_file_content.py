from pathlib import Path
import unittest

from functions import config
from functions.messages.errors import Err
from functions.get_file_content import get_file_content
from tempfile import TemporaryDirectory


class TestGetFileContent(unittest.TestCase):
    def test_double_dot(self):
        assert Err.OUTSIDE_WORK_DIR(".", "..") in get_file_content(".", "..")

    def test_double_dot_slash(self):
        assert Err.OUTSIDE_WORK_DIR(".", "..") in get_file_content(".", "../")

    def test_no_read_permission(self):
        with TemporaryDirectory() as tmpdir:
            main_py = Path(f"{tmpdir}/main.py")
            main_py.write_text("Woooooooooooah there buddy")
            main_py.chmod(000)

            assert Err.NO_PERMISSION_FS(main_py) in get_file_content(tmpdir, "main.py")

    def test_existent_files(self):
        with TemporaryDirectory() as tmpdir:
            main_py = Path(f"{tmpdir}/main.py")
            main_py.write_text("this is the main :D")

            text = get_file_content(tmpdir, "main.py")

            assert "this is the main :D" == text

    def test_with_directory(self):
        with TemporaryDirectory() as tmpdir:
            test_dir_p = Path(tmpdir / Path("test_dir"))
            test_dir_p.mkdir()
            assert "is not a file" in get_file_content(tmpdir, "test_dir")

    def test_non_existent_file(self):
        with TemporaryDirectory() as tmpdir:
            cwd_p = Path(tmpdir)
            file_p = Path("bin/blah/blee/bloo.txt")
            assert Err.FILE_NOT_FOUND(cwd_p / file_p) in get_file_content(
                str(cwd_p), str(file_p)
            )

    def test_truncation(self):
        txt_p = Path("test_get_file_content_truncation_sample.txt")
        assert (
            f"test_get_file_content_truncation_sample.txt truncated to {config.gfc.N_CHAR} characters"
            in get_file_content(Path(__file__).parent, txt_p)
        )
