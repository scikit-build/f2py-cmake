cmake_minimum_required(VERSION 3.15...4.2)
project(${SKBUILD_PROJECT_NAME} LANGUAGES C Fortran)

find_package(
  Python
  COMPONENTS Interpreter Development.Module NumPy
  REQUIRED)

include(UseF2Py)

# A separate C library the Fortran routine calls into (issue #20).
add_library(adder STATIC adder.c)
set_property(TARGET adder PROPERTY POSITION_INDEPENDENT_CODE ON)

f2py_object_library(f2py_object OBJECT)

f2py_generate_module(mixed mixed.f90 OUTPUT_VARIABLE mixed_files)

python_add_library(mixed MODULE "${mixed_files}" WITH_SOABI)
target_link_libraries(mixed PRIVATE f2py_object adder)

install(TARGETS mixed DESTINATION .)
