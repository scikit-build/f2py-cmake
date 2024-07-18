from __future__ import annotations

import sys
from pathlib import Path

if sys.version_info < (3, 9):
    from importlib_resources import files
else:
    from importlib.resources import files

__all__ = ["vendorize"]


def __dir__() -> list[str]:
    return __all__


def vendorize(target: Path) -> None:
    """
    Vendorize files into a directory. Directory must exist.
    """
    if not target.is_dir():
        msg = f"Target directory {target} does not exist"
        raise AssertionError(msg)

    cmake_dir = files("f2py_cmake") / "cmake"

    use = cmake_dir / "UseF2Py.cmake"
    use_target = target / "UseF2Py.cmake"
    use_target.write_text(use.read_text(encoding="utf-8"), encoding="utf-8")
