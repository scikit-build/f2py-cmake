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
also provide the following helper functions:

```cmake
f2py_object_library(<name> <type>)

f2py_generate_signature(<module> <files>...
                  OUTPUT <Signature>
                  [OUTPUT_VARIABLE <OutputVariable>]
                  [NOLOWER]
                  [F2PY_ARGS <args> ...]
                  )

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

# Create the F2Py `numpyobject` library.
f2py_object_library(f2py_object OBJECT)

f2py_generate_module(fibby fib1.f OUTPUT_VARIABLE fibby_files)

python_add_library(fibby MODULE "${fibby_files}" WITH_SOABI)
target_link_libraries(fibby PRIVATE f2py_object)
```

## Signatures

`f2py_generate_signature` generates a `.pyf` signature file from Fortran
sources, which `f2py_generate_module` can then consume as its `<module>`
argument. f2py's `skip:`/`only:` selectors restrict which routines are wrapped;
write them inline among the source files (a `skip:`/`only:` block runs until a
bare `:`):

```cmake
f2py_generate_signature(mymod a.f90 b.f90 "only:" public_api ":"
                        OUTPUT mymod.pyf OUTPUT_VARIABLE mymod_sig)

# The signature defines the interface; a.f90/b.f90 are compiled and linked.
f2py_generate_module(${mymod_sig} a.f90 b.f90 OUTPUT_VARIABLE mymod_files)

python_add_library(mymod MODULE "${mymod_files}" WITH_SOABI)
target_link_libraries(mymod PRIVATE f2py_object)
```

## scikit-build-core

To use this package with scikit-build-core, you need to include it in your build
requirements:

```toml
[build-system]
requires = ["scikit-build-core", "numpy", "f2py-cmake"]
build-backend = "scikit_build_core.build"
```

## Vendoring

You can vendor UseF2Py into your package, as well. This avoids requiring a
dependency at build time and protects you against changes in this package, at
the expense of requiring manual re-vendoring to get bugfixes and/or
improvements. This mechanism is also ideal if you want to support direct builds,
outside of scikit-build-core.

You should make a CMake helper directory, such as `cmake`. Add this to your
`CMakeLists.txt` like this:

```cmake
list(APPEND CMAKE_MODULE_PATH "${CMAKE_SOURCE_DIR}/cmake")
```

Then, you can vendor our file into that folder:

```bash
pipx run f2py-cmake vendor cmake
```

## Acknowledgements

Support for this work was provided by NSF grant [OAC-2209877][]. Any opinions,
findings, and conclusions or recommendations expressed in this material are
those of the author(s) and do not necessarily reflect the views of the National
Science Foundation.

<!-- prettier-ignore-start -->
[actions-badge]:            https://github.com/scikit-build/f2py-cmake/actions/workflows/ci.yml/badge.svg
[actions-link]:             https://github.com/scikit-build/f2py-cmake/actions
[github-discussions-badge]: https://img.shields.io/static/v1?label=Discussions&message=Ask&color=blue&logo=github
[github-discussions-link]:  https://github.com/scikit-build/f2py-cmake/discussions
[oac-2209877]:              https://www.nsf.gov/awardsearch/showAward?AWD_ID=2209877&HistoricalAwards=false
[pypi-link]:                https://pypi.org/project/f2py-cmake/
[pypi-platforms]:           https://img.shields.io/pypi/pyversions/f2py-cmake
[pypi-version]:             https://img.shields.io/pypi/v/f2py-cmake
<!-- prettier-ignore-end -->
