from __future__ import annotations

import importlib.metadata
import shutil
import subprocess
import zipfile
from pathlib import Path

import pytest
from scikit_build_core.build import build_wheel

import f2py_cmake as m
import f2py_cmake.vendor

DIR = Path(__file__).parent.resolve()


def test_version():
    assert importlib.metadata.version("f2py_cmake") == m.__version__


@pytest.mark.skipif(shutil.which("cmake") is None, reason="CMake not found")
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


def test_f90(monkeypatch, tmp_path):
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

    subprocess.run(["cmake", "-S", ".", "-B", str(build_dir)], check=True)
