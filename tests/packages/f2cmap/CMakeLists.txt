cmake_minimum_required(VERSION 3.15...3.29)
project(${SKBUILD_PROJECT_NAME} LANGUAGES C Fortran)

find_package(
  Python
  COMPONENTS Interpreter Development.Module NumPy
  REQUIRED)

include(UseF2Py)

# kinds.f90 uses real(kind=dp); the .f2py_f2cmap next to it (mapping dp ->
# double) is auto-detected, with no explicit F2CMAP argument.
f2py_add_module(kinds kinds.f90)

install(TARGETS kinds DESTINATION .)
