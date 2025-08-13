import os
import unittest
from os import stat_result
from pathlib import Path
from stat import *

from functions.utils import sanitize_path


def is_hidden(dir: Path | str) -> bool:
    if isinstance(dir, str):
        dir = Path(dir)
    return len([part for part in dir.parts if part.startswith(".")]) > 0


def dir_size(path: Path | str, ignore_dot=True) -> int:
    if isinstance(path, str):
        path = Path(path)
    size = 0
    if path.is_dir():
        for f in path.iterdir():
            if ignore_dot and is_hidden(f):
                continue
            size += dir_size(f)
    else:
        size += path.stat().st_size
    return size


def get_files_info(cwd: str, sub_dir: str = "") -> str:
    if sub_dir != "":
        try:
            sanitize_path(sub_dir)
        except ValueError as err:
            return err.args[0]
    info_dir = Path(os.path.join(cwd, sub_dir))
    if info_dir.name == "":
        cwd = info_dir.absolute().as_posix()
        info_dir = info_dir.absolute()
    if info_dir.parts[0] != cwd:
        return f"error: cannot list {info_dir} because it is outside of the working directory {cwd}"

    info: list[str] = []
    for f in info_dir.iterdir():
        f_info = f"- {f.name}: file_size={dir_size(f)} is_dir={f.is_dir()}"
        info.append(f_info)
    return "\n".join(info)
