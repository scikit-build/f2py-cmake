from __future__ import annotations

import importlib.metadata
import zipfile
from pathlib import Path

from scikit_build_core.build import build_wheel

import f2py_cmake as m

DIR = Path(__file__).parent.resolve()


def test_version():
    assert importlib.metadata.version("f2py_cmake") == m.__version__


def test_f77(monkeypatch, tmp_path):
    monkeypatch.chdir(DIR / "packages/f77")
    build_dir = tmp_path / "build"

    wheel = build_wheel(
        str(tmp_path), {"build-dir": str(build_dir), "wheel.license-files": []}
    )

    with zipfile.ZipFile(tmp_path / wheel) as f:
        file_names = set(f.namelist())
    assert len(file_names) == 4

    build_files = {x.name for x in build_dir.iterdir()}
    assert "fibbymodule.c" in build_files
    assert "fibby-f2pywrappers.f" in build_files
