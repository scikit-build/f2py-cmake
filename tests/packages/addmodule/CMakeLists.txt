cmake_minimum_required(VERSION 3.15...4.2)
project(${SKBUILD_PROJECT_NAME} LANGUAGES C Fortran)

find_package(
  Python
  COMPONENTS Interpreter Development.Module NumPy
  REQUIRED)

include(UseF2Py)

f2py_add_module(fibby fib1.f)

install(TARGETS fibby DESTINATION .)
