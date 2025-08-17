import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from functions.messages.info import Info
from functions.write_file import write_file


class TestWriteFile(unittest.TestCase):

    def test_create_file(self):
        with TemporaryDirectory() as tmpdir:
            test_p = Path(tmpdir) / Path("not_here.txt")
            test_txt = "Open Sesame"
            write_file(tmpdir, test_p.name, test_txt)
            assert test_p.exists()

    def test_write_text(self):
        with TemporaryDirectory() as tmpdir:
            test_p = Path(tmpdir) / Path("not_here.txt")
            test_txt = "Open Sesame"
            msg = Info.WROTE_FILE(Path(tmpdir) / test_p, len(test_txt))
            assert msg in write_file(tmpdir, test_p.name, test_txt)
            assert test_txt == test_p.read_text()
