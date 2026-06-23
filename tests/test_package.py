from __future__ import annotations

import importlib.metadata
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

import pytest
from scikit_build_core.build import build_wheel

import f2py_cmake as m
import f2py_cmake.vendor

DIR = Path(__file__).parent.resolve()
CMAKE = shutil.which("cmake")


def test_version() -> None:
    assert importlib.metadata.version("f2py_cmake") == m.__version__


@pytest.mark.skipif(CMAKE is None, reason="CMake not found")
def test_f77(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
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


@pytest.mark.skipif(CMAKE is None, reason="CMake not found")
def test_signature(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.chdir(DIR / "packages/sig")
    build_dir = tmp_path / "build"

    build_wheel(str(tmp_path), {"build-dir": str(build_dir), "wheel.license-files": []})

    build_files = {x.name for x in build_dir.iterdir()}
    assert "mymod.pyf" in build_files
    assert "mymodmodule.c" in build_files

    signature = (build_dir / "mymod.pyf").read_text()
    assert "keep_me" in signature
    assert "drop_me" not in signature
    # helper.f90 is linked but not part of the signature.
    assert "compute" not in signature


@pytest.mark.skipif(CMAKE is None, reason="CMake not found")
def test_f90(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    assert CMAKE is not None
    src_dir = tmp_path / "source"
    build_dir = tmp_path / "build"
    shutil.copytree(DIR / "packages/f90dual", src_dir)
    monkeypatch.chdir(src_dir)

    cmake_dir = src_dir / "cmake"
    cmake_dir.mkdir()
    f2py_cmake.vendor.vendorize(cmake_dir)

    inner_cmake_dir = src_dir / "src/subrepo/cmake"
    inner_cmake_dir.mkdir()
    f2py_cmake.vendor.vendorize(inner_cmake_dir)

    subprocess.run(
        [CMAKE, "-S", ".", "-B", build_dir, f"-DPython_ROOT={sys.prefix}"],
        check=True,
    )
