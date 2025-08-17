import os
from pathlib import Path

from .utils import check_path_safety


def is_hidden(dir: Path | str) -> bool:
    if isinstance(dir, str):
        dir = Path(dir)
    return len([part for part in dir.parts if part.startswith(".")]) > 0


def dir_size(path: Path | str, ignore_dot=True) -> int:
    if isinstance(path, str):
        path = Path(path)
    size = 0
    if path.is_dir() and not path.is_symlink():
        for f in path.iterdir():
            if ignore_dot and is_hidden(f):
                continue
            size += dir_size(f, ignore_dot)
    else:
        # we open the file here file to make sure we can read it (triggering)
        # exceptions that are bubbled up to get_files_info
        with path.open() as buf:
            size += path.stat().st_size
    return size


def get_files_info(cwd: str, sub_dir: str = "") -> str:
    if sub_dir != "":
        combned_path = Path(cwd).joinpath(Path(sub_dir))
        if not combned_path.exists():
            return f"error: directory does not exist {combned_path.absolute()}"
        try:
            check_path_safety(sub_dir, cwd)
        except ValueError as err:
            return err.args[0]

    target_dir = Path(os.path.join(cwd, sub_dir))

    info: list[str] = []
    try:
        for f in target_dir.iterdir():
            f_info = f"- {f.name}: file_size={dir_size(f)} is_dir={f.is_dir()}"
            info.append(f_info)
    except FileNotFoundError as err:
        return f"error: file not found {err.filename}"
    except PermissionError as err:
        return f"error: no permission for reading file {err.filename}"
    except OSError as err:
        return f"error: unknown exception - {err}"

    return "\n".join(info)
