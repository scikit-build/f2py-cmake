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
`F2Py::Headers` target and provide the following helper functions:

```cmake
f2py_object_library(<name> <type>)

f2py_generate_signature(<module> <files>...
                  OUTPUT <Signature>
                  [ONLY <functions> ...]
                  [SKIP <functions> ...]
                  [OUTPUT_VARIABLE <OutputVariable>]
                  [F2CMAP <file>]
                  [NOLOWER]
                  [F2PY_ARGS <args> ...]
                  )

f2py_generate_module(<module> <files>...
                  [F2PY_ARGS <args> ...]
                  [F77 | F90]
                  [NOLOWER]
                  [F2CMAP <file>]
                  [OUTPUT_DIR <OutputDir>]
                  [OUTPUT_VARIABLE <OutputVariable>]
                  )

f2py_add_module(<name> <files>...
                  [F2PY_ARGS <args> ...]
                  [F77 | F90]
                  [NOLOWER]
                  [OUTPUT_DIR <OutputDir>]
                  )
```

## Example

`f2py_add_module` builds an importable extension module in a single call. It
generates the wrappers, creates the Python module target, and compiles/links the
F2Py `fortranobject` support for you:

```cmake
find_package(
  Python
  COMPONENTS Interpreter Development.Module NumPy
  REQUIRED)

include(UseF2Py)

f2py_add_module(fibby fib1.f)
```

`<name>` may instead be a `.pyf` signature path (as accepted by
`f2py_generate_module`); the module name is taken from the file stem. The
created target is a normal CMake target named `<name>`, so customize it
afterward with `target_*()` / `set_target_properties()` as usual.

If you need to share a single `fortranobject` library across several modules, or
want the generated sources for custom wiring, use the primitives directly:

```cmake
# Create the F2Py `numpyobject` library.
f2py_object_library(f2py_object OBJECT)

f2py_generate_module(fibby fib1.f OUTPUT_VARIABLE fibby_files)

python_add_library(fibby MODULE "${fibby_files}" WITH_SOABI)
target_link_libraries(fibby PRIVATE f2py_object)
```

## Signatures

`f2py_generate_signature` generates a `.pyf` signature file from Fortran
sources, which `f2py_generate_module` can then consume as its `<module>`
argument. `ONLY` and `SKIP` restrict which routines are wrapped (a thin wrapper
over f2py's `only:`/`skip:` selectors):

```cmake
f2py_generate_signature(mymod a.f90 b.f90
                        ONLY public_api
                        OUTPUT mymod.pyf OUTPUT_VARIABLE mymod_sig)

# The signature defines the interface; a.f90/b.f90 are compiled and linked.
f2py_generate_module(${mymod_sig} a.f90 b.f90 OUTPUT_VARIABLE mymod_files)

python_add_library(mymod MODULE "${mymod_files}" WITH_SOABI)
target_link_libraries(mymod PRIVATE f2py_object)
```

The files passed to `f2py_generate_module` need not match those used for the
signature. The signature alone defines the wrapped interface, so you can build
it from a subset and link extra Fortran that is called internally but never
exposed to Python:

```cmake
f2py_generate_signature(mymod a.f90 OUTPUT mymod.pyf OUTPUT_VARIABLE mymod_sig)

# helper.f90 is linked but not wrapped.
f2py_generate_module("${mymod_sig}" a.f90 helper.f90 OUTPUT_VARIABLE mymod_files)
```

## Custom type maps

Fortran code that uses custom kinds (such as `real(kind=dp)`) needs a
`.f2py_f2cmap` file telling f2py how to map those kinds to C types, e.g.:

```python
dict(real=dict(dp="double"))
```

A `.f2py_f2cmap` placed next to your sources is auto-detected by both
`f2py_generate_signature` and `f2py_generate_module`. You can also point at one
explicitly with `F2CMAP <file>` (a relative path is resolved against the current
source directory, and an explicit `F2CMAP` overrides auto-detection):

```cmake
f2py_generate_module(mymod mymod.f90 F2CMAP maps/types.f2cmap
                     OUTPUT_VARIABLE mymod_files)
```

f2py's own `--f2cmap` default (the cwd) does not work here: these helpers run
f2py in the build directory, not the source tree, so the file must be located
explicitly.

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
