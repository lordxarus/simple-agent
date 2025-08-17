import sys
import unittest

from functions.utils import get_noimpl_printer, is_relative_path_in_work_dir

noimpl = get_noimpl_printer(__file__)

class TestIsPathInWorkDir(unittest.TestCase):

    def test_double_dot(self):
        assert not is_relative_path_in_work_dir(".", "..")

    def test_double_dot_slash(self):
        assert not is_relative_path_in_work_dir(".", "../")

    def test_reltve_work_dir_abslte_sub_dir(self):
        noimpl("test_reltve_work_dir_abslte_sub_dir")
    def test_abslte_work_dir_reltve_sub_dir(self):
        noimpl("test_abslte_work_dir_reltve_sub_dir")
    def test_reltve_work_dir_reltve_sub_dir(self):
        noimpl("test_reltve_work_dir_reltve_sub_dir")
    """
    Platform specific tests
    """

    def test_slash_bin(self):
        if sys.platform != "win32":
            assert not is_relative_path_in_work_dir("calculator", "/bin")
