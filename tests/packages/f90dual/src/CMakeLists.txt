add_subdirectory(subrepo)

set (CMAKE_FIND_FRAMEWORK LAST)
find_package(
  Python
  COMPONENTS Interpreter Development.Module NumPy
  REQUIRED)

include(UseF2Py)

message(STATUS "Building test f2py module")

f2py_object_library(test_object OBJECT)
f2py_generate_module(test_ test_py.F90 OUTPUT_VARIABLE test_files)
# .F90 is free-form Fortran: auto-detection must select the F90 path and declare
# the -f2pywrappers2.f90 output despite the uppercase extension (gh-57 item 2).
if(NOT test_files MATCHES "test_-f2pywrappers2\\.f90")
  message(FATAL_ERROR "Expected F90 wrapper for .F90 source, got: ${test_files}")
endif()
python_add_library(test_ MODULE "${test_files}" WITH_SOABI)
target_link_libraries(test_ PRIVATE test_object)
install(TARGETS test_ DESTINATION lib/Python)

message(STATUS "Done building test f2py module")
