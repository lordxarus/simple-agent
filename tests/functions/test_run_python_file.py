from types import FunctionType
import unittest
from tempfile import TemporaryDirectory
from pathlib import Path

from functions.messages.info import Info
from functions.utils import get_noimpl_printer
from functions.run_python_file import run_python_file


noimpl = get_noimpl_printer(__file__)


class TestRunPythonFile(unittest.TestCase):

    def test_empty_file(self):
        noimpl("empty_file")

    def test_no_permission(self):
        noimpl("no_permission")

    def test_run_script(self):
        with TemporaryDirectory() as tmpdir:
            script_p = Path(tmpdir) / Path("test.py")
            script_p.write_text('print("hello world")')
            assert "output from: test.py" in run_python_file(tmpdir, script_p)

    def test_bad_script(self):
        with TemporaryDirectory() as tmpdir:
            script_p = Path(tmpdir) / Path("test.py")
            script_p.write_text('print "hello world")')
            assert f'stderr: File "{script_p}", line 1' in run_python_file(
                tmpdir, script_p
            )
