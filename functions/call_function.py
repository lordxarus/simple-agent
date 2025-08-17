from pathlib import Path
from google.genai import types

from functions.run_python_file import run_python_file
from functions.utils import format_dict
from functions.write_file import write_file
from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info

_funcs = {
    "run_python_file": run_python_file,
    "write_file": write_file,
    "get_file_content": get_file_content,
    "get_files_info": get_files_info,
}


def call_function(
    func_call: types.FunctionCall, work_dir: str | Path, verbose=False
) -> types.Content:
    work_dir = Path(work_dir)

    if func_call.name is None:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name="call_function",
                    response={"error": "no function name given"},
                )
            ],
        )
    name = func_call.name
    args = func_call.args or {}
    args["cwd"] = str(work_dir)

    if verbose:
        print(f"calling function: {name}({format_dict(args)})")
    else:
        print(f"calling function: {name}")

    result: str
    try:
        result = _funcs[name](**args)
    except KeyError:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=name,
                    response={"error": f"Unknown function: {name}"},
                )
            ],
        )
    except TypeError as err:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=name,
                    response={"error": str(err)},
                )
            ],
        )

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=name,
                response={"result": result},
            )
        ],
    )
