import os


def get_print_dbg(debug_env_var="DEBUG", debug_prefix="debug: ", force_enable=False):
    debug: bool = force_enable or False
    if not debug:
        try:
            env_var: str = os.environ[debug_env_var].lower()
            if env_var == "true" or env_var == "1":
                debug = True
        except KeyError:
            pass

    def print_dbg(txt: str):
        if debug:
            print(f"{debug_prefix}{txt}")

    return print_dbg
