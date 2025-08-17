from pathlib import Path
import sys

from functions.messages.info import Info
from .utils import is_relative_path_in_work_dir
from .messages.errors import Err
import subprocess


def run_python_file(
    cwd: str | Path, file_path: str | Path, args: list[str] = []
) -> str:
    cwd = Path(cwd)
    file_path = Path(file_path)

    full_path = cwd / file_path
    full_path_rel = full_path.relative_to(cwd)

    if not is_relative_path_in_work_dir(cwd, file_path):
        return Err.OUTSIDE_WORK_DIR(cwd, file_path)
    if not full_path.exists():
        return Err.FILE_NOT_FOUND(full_path)

    args.insert(0, sys.executable)
    args.insert(1, str(full_path))

    # TODO pass a dict to env parameter that doesn't have Gemini API
    # key included
    # print(args)
    done_proc = subprocess.run(
        args, capture_output=True, timeout=30, encoding="utf-8"
    )
    stdout = done_proc.stdout.strip()
    stderr = done_proc.stderr.strip()
    try:
        done_proc.check_returncode()
    except subprocess.CalledProcessError as err:
        return Err.RUN_PYTHON_FILE_NON_ZERO_EXIT(
            full_path_rel,
            err,
            stdout,
            stderr,
        )

    if len(stderr) > 0 or len(stdout) > 0:
        return Info.RUN_PYTHON_FILE_SUCCESS(full_path_rel, stdout, stderr)
    else:
        return Info.RUN_PYTHON_FILE_NO_OUTPUT(full_path_rel)
