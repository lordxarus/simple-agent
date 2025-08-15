from pathlib import Path


def check_path_safety(sub_dir: str) -> None:
    if sub_dir.startswith("/"):
        raise ValueError('error: sub_dir cannot begin with "/"')
    if len([part for part in Path(sub_dir).parts if part == ".."]) > 0:
        raise ValueError(f'error: sub_dir  cannot contain ".."')


def check_has_at_least(
    has_at_least: list[list[str]], lines: list[str]
) -> tuple[bool, str]:
    """
    Ensures that every string inside has_at_least appears at least once in lines
    """

    found = []
    last_not_found_part = ""
    for line in lines:
        for parts in has_at_least:
            for part in parts:
                if part not in line:
                    last_not_found_part = part
                    break
            found.append(parts)
    import pdb

    # any() expr returns True if all parts were found and False if not
    return (
        not any(parts for parts in has_at_least if parts not in found),
        last_not_found_part,
    )
