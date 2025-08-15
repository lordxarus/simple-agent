from pathlib import Path
import unittest
import os

from functions import get_files_info, utils
from tempfile import NamedTemporaryFile, TemporaryDirectory, TemporaryFile


class TestGetFilesInfo(unittest.TestCase):

    def test_double_dot(self):
        assert get_files_info(".", "..").startswith("error: sub_dir")

    def test_double_dot_slash(self):
        assert get_files_info(".", "../").startswith("error: sub_dir")

    def test_deep_double_dot(self):
        assert get_files_info(".", "functions/../test/../..").startswith(
            "error: sub_dir"
        )

    def test_existent_files(self):
        with TemporaryDirectory() as tmpdir:
            with (
                NamedTemporaryFile(dir=tmpdir) as main_py,
                NamedTemporaryFile(dir=tmpdir) as test_py,
                TemporaryDirectory(dir=tmpdir) as pkg_dir,
                NamedTemporaryFile(dir=pkg_dir),
            ):

                main_py.write(bytes.fromhex("2EF002F004142FDA02"))
                main_py.seek(0)
                main_py_path = Path(main_py.name)

                test_py.write(bytes.fromhex("249BDF"))
                test_py.seek(0)
                test_py_path = Path(test_py.name)

                pkg_dir_path = Path(pkg_dir)
                has_at_least = [
                    [
                        f"- {main_py_path.name}: file_size={Path(main_py.name).stat().st_size} is_dir=False",
                    ],
                    [
                        f"- {test_py_path.name}: file_size={Path(test_py.name).stat().st_size} is_dir=False",
                    ],
                    [f"- {pkg_dir_path.name}: file_size=0 is_dir=True"],
                ]
                lines = get_files_info(tmpdir).splitlines()
                at_least = utils.check_has_at_least(has_at_least, lines)
                assert at_least[0], f"no lines matched fragment {at_least[1]}"

    def test_nonexistent_files(self):
        with TemporaryDirectory() as tmpdir, TemporaryFile() as tmpfile:
            has_at_least = [["- this_isnt_real.py"]]
            files = get_files_info(tmpdir).splitlines()
            at_least = utils.check_has_at_least(has_at_least, files)
            assert not at_least[0]

    def test_empty_dir(self):
        with TemporaryDirectory() as tmpdir:
            has_at_least = [["- this_isnt_real.py"]]
            files = get_files_info(tmpdir).splitlines()
            at_least = utils.check_has_at_least(has_at_least, files)
            assert not at_least[0]

    def test_slash_bin(self):
        assert (
            get_files_info("calculator", "/bin")
            == 'error: sub_dir cannot begin with "/"'
        )

    def test_non_existent(self):
        assert (
            get_files_info("calculator", "./bin/blah/blee/bloo")
            == "error: directory not found calculator/bin/blah/blee/bloo"
        )
