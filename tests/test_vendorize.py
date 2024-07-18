from __future__ import annotations

import sys
from pathlib import Path

import pytest

from f2py_cmake.__main__ import main

DIR = Path(__file__).parent.resolve()
USE_F2PY = DIR.parent.joinpath("src/f2py_cmake/cmake/UseF2Py.cmake").read_text()


def test_copy_files(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    path = tmp_path / "copy_all"
    path.mkdir()

    monkeypatch.setattr(sys, "argv", [sys.executable, "vendor", str(path)])
    main()

    assert path.joinpath("UseF2Py.cmake").read_text() == USE_F2PY
