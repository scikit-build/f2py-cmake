cmake_minimum_required(VERSION 3.15...3.29)
project(${SKBUILD_PROJECT_NAME} LANGUAGES C Fortran)

find_package(
  Python
  COMPONENTS Interpreter Development.Module NumPy
  REQUIRED)

include(UseF2Py)

f2py_object_library(f2py_object OBJECT)

f2py_generate_module(fibby fib1.f OUTPUT_VARIABLE fibby_files)

python_add_library(fibby MODULE "${fibby_files}" WITH_SOABI)
target_link_libraries(fibby PRIVATE f2py_object)

install(TARGETS fibby DESTINATION .)
