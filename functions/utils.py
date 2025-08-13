from pathlib import Path


def check_path_safety(sub_dir: str) -> None:
    if sub_dir.startswith("/"):
        raise ValueError('error: sub_dir cannot begin with "/"')
    if len([part for part in Path(sub_dir).parts if part == ".."]) > 0:
        raise ValueError(f'error: sub_dir  cannot contain ".."')


def check_has_at_least(
    has_at_least: list[str], lines: list[str]
) -> tuple[bool, str | None]:
    """
    Ensures that every string inside has_at_least appears at least once in lines
    """
    for ln in lines:
        for i in range(0, len(has_at_least), 2):
            frag = has_at_least[i]
            second_frag = has_at_least[i + 1]
            if len(ln.split(frag)) > 1 and len(ln.split(second_frag)) > 1:
                break
            elif i + 1 == len(has_at_least) - 1:
                return (False, ln)
    return (True, None)
