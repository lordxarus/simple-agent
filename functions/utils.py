from pathlib import Path
from types import FunctionType


def _noimpl(file: str, func: str) -> str:
    return f"noimpl: function {func}()@{file}"


def get_noimpl_printer(file_path: str) -> FunctionType:
    return lambda func: print(
        f"\n{_noimpl(str(Path(file_path).relative_to(Path().cwd())), func)}"
    )


def format_dict(dict: dict) -> str:
    return ", ".join([f"{key}={val}" for key, val in dict.items()])


def is_relative_path_in_work_dir(work_dir: str | Path, path: str | Path) -> bool:
    work_dir = Path(work_dir)
    path = Path(path)
    pps = path.parts
    # return not pps[0] == ".." and
    #
    # and pps[0].startswith(".")
    if len(pps) == 1:
        if pps[0] == "..":
            return False
    #     path = work_dir / path
    return (work_dir / path).is_relative_to(work_dir)


def is_hidden(dir: str | Path) -> bool:
    dir = Path(dir)
    return len([part for part in dir.parts if part.startswith(".")]) > 0


def dir_size(path: str | Path, ignore_dot=True) -> int:
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
        with path.open():
            size += path.stat().st_size
    return size


def does_each_appear(
    has_at_least: list[list[str]], lines: list[str]
) -> tuple[bool, str]:
    """
    Ensures that every string inside has_at_least appears at least once in lines
    """

    found = []
    last_not_found_part = ""
    for line in lines:
        for parts in has_at_least:
            for i, part in enumerate(parts):
                if part not in line or part != line:
                    last_not_found_part = part
                    break
                elif i == len(parts) - 1:
                    found.append(parts)
    # any() expr returns True if all parts were found and False if not
    return (
        not any(parts for parts in has_at_least if parts not in found),
        last_not_found_part,
    )
