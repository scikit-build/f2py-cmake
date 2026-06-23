# Agent instructions

## What this is

`f2py-cmake` ships CMake helpers for building NumPy F2Py (Fortran) extension
modules. The substance of the project is a single CMake module,
`src/f2py_cmake/cmake/UseF2Py.cmake`; the Python package is a thin wrapper that
makes that file discoverable to CMake and vendorable into other projects.

## Architecture

Two distinct distribution paths feed off the same `UseF2Py.cmake` file:

1. **Build-time dependency.** Listing `f2py-cmake` in `[build-system].requires`
   registers `f2py_cmake.cmake` via the `cmake.module` entry point (see
   `pyproject.toml`). scikit-build-core then adds the package's `cmake/`
   directory to `CMAKE_MODULE_PATH`, so `include(UseF2Py)` resolves. The Python
   module `cmake/__init__.py` is intentionally empty — it exists only to mark
   the package directory for the entry point.

2. **Vendoring.** `f2py-cmake vendor <dir>` (`__main__.py` → `vendor.py`) copies
   `UseF2Py.cmake` into a target directory so a project can build without the
   runtime dependency. `vendorize()` uses `importlib.resources.files` to locate
   the bundled CMake file. There is no templating — it is a verbatim copy, which
   `tests/test_vendorize.py` asserts byte-for-byte.

`UseF2Py.cmake` defines the public CMake API: the `F2Py::Headers` target,
`f2py_object_library()`, and `f2py_generate_module()`. It auto-detects whether
`Python` or `Python3` was found (requiring the NumPy component) and shells out
to `numpy.f2py.get_include()` to locate `fortranobject.c/.h`.
`f2py_generate_module()` auto-selects F77 vs F90 from file extensions unless
`F77`/`F90` is passed; this controls which f2py wrapper files
(`*-f2pywrappers.f`, `*-f2pywrappers2.f90`) are declared as build outputs.

When editing `UseF2Py.cmake`, keep the minimum CMake version (3.17) consistent
with the `FATAL_ERROR` guard at the top of the file.

## Commands

Run inside the package with `uv run` (e.g. `uv run pytest`).

- `nox` — lint + tests across installed Pythons.
- `nox -s lint` — pre-commit hooks only. Prefer `prek -a --quiet` for ad-hoc
  linting.
- `nox -s tests` — pytest.
- `nox -s pylint` — pylint (installs the package; slower than the pre-commit
  checks).
- `nox -s build` — build SDist and wheel.
- `uv run pytest tests/test_vendorize.py::test_copy_files` — run a single test.

The CMake-driven tests (`test_f77`, `test_f90` in `tests/test_package.py`) are
skipped automatically when `cmake` is not on `PATH`. `test_f77` builds a wheel
through scikit-build-core; `test_f90` vendors the CMake module into a nested
project layout and configures it.

## Test fixtures

`tests/packages/` holds real mini-projects used as build fixtures:

- `f77/` — single `.f` file built into a wheel via scikit-build-core.
- `f90dual/` — nested-subrepo layout exercising vendoring into multiple
  directories and the F90 path.

## Conventions

- Python target is 3.8+; code uses `from __future__ import annotations`.
- Lint is Ruff with `select = ["ALL"]` (see `pyproject.toml` for the few
  ignores), plus strict mypy. Tests run with `filterwarnings = ["error"]`.
- Version is derived from git tags via `hatch-vcs`; `_version.py` is generated,
  never edit it.

## Packaging note

`.distro/`, `.fmf/`, `.packit.yaml`, and `tests/*.fmf` are Fedora RPM packaging
(packit / tmt) and run in that CI separately — not part of normal local dev.
