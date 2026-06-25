cmake_minimum_required(VERSION 3.15...4.2)
project(${SKBUILD_PROJECT_NAME} LANGUAGES C Fortran)

find_package(
  Python
  COMPONENTS Interpreter Development.Module NumPy
  REQUIRED)

include(UseF2Py)

# Drive the one-shot helper from a checked-in signature file. The .pyf path is
# stripped to the real module name (mymod) for the target and library.
f2py_add_module(mymod.pyf mymod.f90)

install(TARGETS mymod DESTINATION .)
