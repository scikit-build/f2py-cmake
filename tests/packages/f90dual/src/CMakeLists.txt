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
python_add_library(test_ MODULE "${test_files}" WITH_SOABI)
target_link_libraries(test_ PRIVATE test_object)
install(TARGETS test_ DESTINATION lib/Python)

message(STATUS "Done building test f2py module")
