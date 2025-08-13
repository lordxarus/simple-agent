from typing import Self
import os

def get_print_dbg(debug_env_var="DEBUG", debug_prefix="debug: "):
    debug: bool = False
    try:
        env_var: str = os.environ[debug_env_var].lower()
        if env_var == "true" or env_var == "1":
            debug = True
    except KeyError:
        ()

    def print_dbg(txt: str):
        if debug:
            print(f"{debug_prefix}{txt}")

    return print_dbg
