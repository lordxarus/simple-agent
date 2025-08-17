class Info:
    WROTE_FILE = lambda path, n_chars: f"info: wrote {n_chars} characters to {path}"
    RUN_PYTHON_FILE_SUCCESS = (
        lambda path, stdout, stderr: f"output from: {path}\nstdout: {stdout}\nstderr: {stderr}"
    )
    RUN_PYTHON_FILE_NO_OUTPUT = lambda path: f"info: no output after running {path}"
