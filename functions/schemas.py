from google.genai import types


get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "sub_dir": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)
get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads text from the specified file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path of the file to read, relative to the working directory",
            ),
        },
    ),
)
write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write text to a file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path of the file to write to, relative to the working directory.",
            ),
            "text": types.Schema(
                type=types.Type.STRING,
                description="The file's new contents. All previous text will be overwritten.",
            ),
        },
    ),
)
run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run a Python script with the current interpreter.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path of the script to run, relative to the working directory",
            ),
        },
    ),
)
