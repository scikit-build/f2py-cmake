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
def test_add_module(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.chdir(DIR / "packages/addmodule")
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
def test_add_module_pyf(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.chdir(DIR / "packages/addmodulepyf")
    build_dir = tmp_path / "build"

    build_wheel(str(tmp_path), {"build-dir": str(build_dir), "wheel.license-files": []})

    build_files = {x.name for x in build_dir.iterdir()}
    assert "mymodmodule.c" in build_files


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
def test_cmix(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    # A Fortran module that calls into a separate C library (issue #20). The
    # original source must be compiled in and the C library linked, or the
    # built module fails to import with an undefined symbol. Building isn't
    # enough to catch this on macOS (-undefined dynamic_lookup), so import it.
    monkeypatch.chdir(DIR / "packages/cmix")
    build_dir = tmp_path / "build"

    wheel = build_wheel(
        str(tmp_path), {"build-dir": str(build_dir), "wheel.license-files": []}
    )

    install_dir = tmp_path / "install"
    with zipfile.ZipFile(tmp_path / wheel) as f:
        f.extractall(install_dir)

    monkeypatch.syspath_prepend(str(install_dir))
    try:
        mixed = importlib.import_module("mixed")
        assert mixed.add_them(2.0, 3.0) == pytest.approx(5.0)
    finally:
        sys.modules.pop("mixed", None)


@pytest.mark.skipif(CMAKE is None, reason="CMake not found")
def test_f2cmap(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    # kinds.f90 uses real(kind=dp); without the .f2py_f2cmap mapping dp to
    # double, f2py can't wrap scale_dp. The file lives next to the sources and
    # is auto-detected (no explicit F2CMAP arg), so the build and import only
    # succeed if the source-tree .f2py_f2cmap is found.
    monkeypatch.chdir(DIR / "packages/f2cmap")
    build_dir = tmp_path / "build"

    wheel = build_wheel(
        str(tmp_path), {"build-dir": str(build_dir), "wheel.license-files": []}
    )

    install_dir = tmp_path / "install"
    with zipfile.ZipFile(tmp_path / wheel) as f:
        f.extractall(install_dir)

    monkeypatch.syspath_prepend(str(install_dir))
    try:
        # Without the auto-detected .f2py_f2cmap, f2py maps dp to C float and
        # the dp Fortran argument is fed a single-precision value, losing
        # precision. A value that only round-trips through double exactly
        # confirms dp was mapped to double.
        kinds = importlib.import_module("kinds")
        x = 0.1
        assert kinds.kinds.scale_dp(x) == pytest.approx(0.2, abs=1e-15)
    finally:
        sys.modules.pop("kinds", None)


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
