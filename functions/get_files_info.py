from pathlib import Path

from functions.errors import Err

from .utils import is_path_in_work_dir, dir_size


def get_files_info(cwd: str | Path, sub_dir: str | Path = Path("")) -> str:
    cwd = Path(cwd)
    sub_dir = Path(sub_dir)

    # we assume that cwd is valid and only check if sub_dir exists if it
    # has been passed to us
    if any(sub_dir.parts):
        combined = cwd / sub_dir
        if not combined.exists():
            return Err.DIRECTORY_NOT_FOUND(combined)
        if not is_path_in_work_dir(cwd, sub_dir):
            return Err.OUTSIDE_WORK_DIR(cwd, sub_dir)

    target_dir = cwd / sub_dir

    info: list[str] = []
    try:
        for f in target_dir.iterdir():
            f_info = f"- {f.name}: file_size={dir_size(f)} is_dir={f.is_dir()}"
            info.append(f_info)
    except FileNotFoundError as err:
        return Err.FILE_NOT_FOUND(err.filename)
    except PermissionError as err:
        return Err.NO_PERMISSION_FS(err.filename)
    except OSError as err:
        return Err.UNKNOWN(err)

    return "\n".join(info)
