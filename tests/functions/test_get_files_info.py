from pathlib import Path
import unittest

from functions.errors import Err
from functions.get_files_info import get_files_info
from functions.utils import does_each_appear
from tempfile import TemporaryDirectory


class TestGetFilesInfo(unittest.TestCase):

    def test_no_read_permission(self):
        with TemporaryDirectory() as tmpdir:
            main_py = Path(f"{tmpdir}/main.py")
            main_py.touch()
            main_py.chmod(000)
            assert Err.NO_PERMISSION_FS(main_py) in get_files_info(tmpdir)

    def test_existent_files(self):
        with TemporaryDirectory() as tmpdir:
            main_py = Path(f"{tmpdir}/main.py")
            main_py.write_text("this is the main :D")

            test_py = Path(f"{tmpdir}/test.py")
            test_py.write_text("these are really some tests" * 10)

            pkg_dir = Path(f"{tmpdir}/pkg")
            pkg_dir.mkdir()
            has_at_least = [
                [
                    f"- {main_py.name}: file_size={main_py.stat().st_size} is_dir=False",
                ],
                [
                    f"- {test_py.name}: file_size={test_py.stat().st_size} is_dir=False",
                ],
                [f"- {pkg_dir.name}: file_size=0 is_dir=True"],
            ]
            files = get_files_info(tmpdir).splitlines()

            has_at_least.sort()
            files.sort()
            at_least = does_each_appear(has_at_least, files)
            assert at_least[0], f"no lines matched fragment {at_least[1]}"

    def test_empty_dir(self):
        with TemporaryDirectory() as tmpdir:
            has_at_least = [["- this_isnt_real.py"]]
            files = get_files_info(tmpdir).splitlines()

            files.sort()
            has_at_least.sort()

            at_least = does_each_appear(has_at_least, files)
            assert not at_least[0]

    def test_non_existent_sub_dir(self):
        with TemporaryDirectory() as tmpdir:
            cwd_p = Path(tmpdir)
            dir_p = Path("./bin/blah/blee/bloo")
            assert Err.DIRECTORY_NOT_FOUND(cwd_p / dir_p) in get_files_info(
                str(cwd_p), str(dir_p)
            )
