from pathlib import Path

from functions.messages.errors import Err
from .messages.info import Info


def write_file(cwd: str | Path, file_path: str | Path, text: str) -> str:
    cwd = Path(cwd)
    file_path = Path(file_path)

    combined = cwd / file_path

    if not combined.exists():
        try:
            combined.touch()
        except IsADirectoryError as err:
            return Err.EXPECTED_FILE(err.filename)
        except PermissionError as err:
            return Err.NO_PERMISSION_FS(err.filename)
        except OSError as err:
            return Err.UNKNOWN(err)

    # I think it's safe to assume at this point we can access the file_path
    with combined.open(mode="wt") as file:
        file.write(text)
        return Info.WROTE_FILE(combined, len(text))
