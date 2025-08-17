from pathlib import Path


def is_path_in_work_dir(work_dir: str | Path, path: str | Path) -> bool:
    return Path(path).is_relative_to(Path(work_dir).absolute())


def does_each_appear(
    has_at_least: list[list[str]], lines: list[str]
) -> tuple[bool, str]:
    """
    Ensures that every string inside has_at_least appears at least once in lines
    """

    found = []
    last_not_found_part = ""
    for line in lines:
        for parts in has_at_least:
            for i, part in enumerate(parts):
                if part not in line or part != line:
                    last_not_found_part = part
                    break
                elif i == len(parts) - 1:
                    found.append(parts)
    # any() expr returns True if all parts were found and False if not
    return (
        not any(parts for parts in has_at_least if parts not in found),
        last_not_found_part,
    )
