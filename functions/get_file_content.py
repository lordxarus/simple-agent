from functions.utils import is_path_in_work_dir
from pathlib import Path

from .config import gfc as config


def get_file_content(cwd: str, file_path: str) -> str:
    cwd_p = Path(cwd)
    file_p = Path(file_path)
    combined: Path = cwd_p / file_p
    if not combined.exists():
        return f"error: file {combined} does not exist"
    if not is_path_in_work_dir(cwd, file_path):
        return f"error: {file_p} is outside of {cwd_p}"
    if not (cwd_p / file_p).is_file():
        return f"error: {file_p} is not a file"
    try:
        with combined.open() as file:
            text: str = file.read()
            if len(text) <= config.N_CHAR:
                return text

            trunc_msg = f"{file.name} truncated to {config.N_CHAR} characters"
            trunced = text[: config.N_CHAR]
            trunced = trunced[: -len(trunc_msg)]
            trunced += trunc_msg
            print(trunced)
            return trunced

    except FileNotFoundError as err:
        return f"error: file not found {err.filename}"
    except PermissionError as err:
        return f"error: no permission for reading file {err.filename}"
    except OSError as err:
        return f"error: unknown exception - {err}"
