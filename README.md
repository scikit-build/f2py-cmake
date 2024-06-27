# f2py-cmake

[![Actions Status][actions-badge]][actions-link]

<!--
[![Documentation Status][rtd-badge]][rtd-link]
-->

[![PyPI version][pypi-version]][pypi-link]
[![PyPI platforms][pypi-platforms]][pypi-link]

<!--
[![GitHub Discussion][github-discussions-badge]][github-discussions-link]
-->

<!-- SPHINX-START -->

This provides helpers for using F2Py. Use:

```cmake
include(UseF2Py)
```

You must have found a Python interpreter beforehand. This will define a
`F2Py::F2Py` target (along with a matching `F2PY_EXECUTABLE` variable). It will
also provide the following helper function:

```cmake
f2py_generate_module(<module> <files>...
                  [F2PY_ARGS <args> ...]
                  [F77 | F90]
                  [NOLOWER]
                  [OUTPUT_DIR <OutputDir>]
                  [OUTPUT_VARIABLE <OutputVariable>]
                  )
```

## Example

```cmake
find_package(
  Python
  COMPONENTS Interpreter Development.Module NumPy
  REQUIRED)

include(UseF2Py)

f2py_object_library(f2py_object OBJECT)

f2py_generate_module(fibby fib1.f OUTPUT_VARIABLE fibby_files)

python_add_library(fibby MODULE "${fibby_files}" WITH_SOABI)
target_link_library(fibby PRIVATE f2py_object)
```

## scikit-build-core

To use this package with scikit-build-core, you need to include it in your build
requirements:

```toml
[build-system]
requires = ["scikit-build-core", "numpy", "f2py-cmake"]
build-backend = "scikit_build_core.build"
```

<!-- prettier-ignore-start -->
[actions-badge]:            https://github.com/scikit-build/f2py-cmake/workflows/CI/badge.svg
[actions-link]:             https://github.com/scikit-build/f2py-cmake/actions
[github-discussions-badge]: https://img.shields.io/static/v1?label=Discussions&message=Ask&color=blue&logo=github
[github-discussions-link]:  https://github.com/scikit-build/f2py-cmake/discussions
[pypi-link]:                https://pypi.org/project/f2py-cmake/
[pypi-platforms]:           https://img.shields.io/pypi/pyversions/f2py-cmake
[pypi-version]:             https://img.shields.io/pypi/v/f2py-cmake
[rtd-badge]:                https://readthedocs.org/projects/f2py-cmake/badge/?version=latest
[rtd-link]:                 https://f2py-cmake.readthedocs.io/en/latest/?badge=latest

<!-- prettier-ignore-end -->
