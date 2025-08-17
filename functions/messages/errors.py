class Err:
    FILE_NOT_FOUND = lambda path: f"error: file {path} does not exist"
    DIRECTORY_NOT_FOUND = lambda path: f"error: directory not found {path}"
    EXPECTED_FILE = lambda path: f"error: {path} is not a file"
    OUTSIDE_WORK_DIR = (
        lambda work_dir, path: f"error: {path} is outside of allowed working directory: {work_dir}"
    )
    NO_PERMISSION_FS = lambda path: f"error: no permission for reading file {path}"
    RUN_PYTHON_FILE_NON_ZERO_EXIT = (
        lambda path, exception, stdout, stderr: f"error: {exception} while executing {path}\nstdout: {stdout}\nstderr: {stderr}"
    )

    UNKNOWN = lambda err: f"error: unknown exception {err}"
