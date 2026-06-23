cmake_minimum_required(VERSION 3.15...3.29)
project(${SKBUILD_PROJECT_NAME} LANGUAGES C Fortran)

find_package(
  Python
  COMPONENTS Interpreter Development.Module NumPy
  REQUIRED)

include(UseF2Py)

f2py_object_library(f2py_object OBJECT)

# Generate a signature that wraps only keep_me, then build the module from it.
f2py_generate_signature(mymod mymod.f90
                        SKIP drop_me
                        OUTPUT mymod.pyf OUTPUT_VARIABLE mymod_sig)

f2py_generate_module(${mymod_sig} mymod.f90 OUTPUT_VARIABLE mymod_files)

python_add_library(mymod MODULE "${mymod_files}" WITH_SOABI)
target_link_libraries(mymod PRIVATE f2py_object)

install(TARGETS mymod DESTINATION .)
