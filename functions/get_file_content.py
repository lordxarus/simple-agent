from functions.messages.errors import Err
from functions.utils import is_relative_path_in_work_dir
from pathlib import Path

from .config import gfc as config


def get_file_content(cwd: str | Path, file_path: str | Path) -> str:
    cwd_p = Path(cwd)
    file_p = Path(file_path)
    combined: Path = cwd_p / file_p
    if not combined.exists():
        return Err.FILE_NOT_FOUND(combined)
    if not is_relative_path_in_work_dir(cwd, file_path):
        return Err.OUTSIDE_WORK_DIR(cwd_p, file_p)
    if not (combined).is_file():
        return Err.EXPECTED_FILE(combined)
    try:
        with combined.open() as file:
            text: str = file.read()
            if len(text) <= config.N_CHAR:
                return text

            trunc_msg = f"{file.name} truncated to {config.N_CHAR} characters"
            trunced = text[: config.N_CHAR]
            trunced = trunced[: -len(trunc_msg)]
            trunced += trunc_msg
            return trunced

    except FileNotFoundError as err:
        return Err.FILE_NOT_FOUND(err.filename)
    except PermissionError as err:
        return Err.NO_PERMISSION_FS(err.filename)
    except OSError as err:
        return Err.UNKNOWN(err)
