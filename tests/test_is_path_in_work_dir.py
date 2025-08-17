import sys
import unittest

from functions.utils import is_path_in_work_dir


class TestIsPathInWorkDir(unittest.TestCase):

    def test_double_dot(self):
        assert not is_path_in_work_dir(".", "..")

    def test_double_dot_slash(self):
        assert not is_path_in_work_dir(".", "../")

    """
    Platform specific tests
    """

    def test_slash_bin(self):
        if sys.platform != "win32":
            assert not is_path_in_work_dir("calculator", "/bin")
