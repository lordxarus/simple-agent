from abc import abstractclassmethod
import unittest
from ..get_files_info import get_files_info
from ..utils import check_has_at_least



class TestGetFilesInfo(unittest.TestCase):

    def test_double_dot(self):
        assert get_files_info(".", "..").startswith("error: sub_dir")

    def test_double_dot_slash(self):
        assert get_files_info(".", "../").startswith("error: sub_dir")

    def test_deep_double_dot(self):
        assert get_files_info(".", "functions/../test/../..").startswith(
            "error: sub_dir"
        )

    def test_calc_dir(self):
        has_at_least = [
            "- main.py: file_size=",
            "is_dir=False",
            "- tests.py: file_size=",
            "is_dir=False",
            "- pkg: file_size=",
            "is_dir=True",
        ]
        lines = get_files_info("calculator").splitlines()
        at_least = check_has_at_least(has_at_least, lines)
        if not at_least[0]:
            raise ValueError(f"no valid fragments found for line: {at_least[1]}")

    def test_slash_bin(self):
        assert (
            get_files_info("calculator", "/bin")
            == 'error: sub_dir cannot begin with "/"'
        )
