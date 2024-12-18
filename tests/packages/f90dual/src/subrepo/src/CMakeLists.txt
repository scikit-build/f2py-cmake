set(CMAKE_FIND_FRAMEWORK LAST)

find_package(
  Python
  COMPONENTS Interpreter Development.Module NumPy
  REQUIRED)

include(UseF2Py)

message(STATUS "Building subrepo f2py module")

f2py_object_library(subrepo_object OBJECT)
f2py_generate_module(subrepo_ subrepo_py.F90 OUTPUT_VARIABLE subrepo_files)
python_add_library(subrepo_ MODULE "${subrepo_files}" WITH_SOABI)
target_link_libraries(subrepo_ PRIVATE subrepo_object)
install(TARGETS subrepo_ DESTINATION lib/Python)

message(STATUS "Done building subrepo f2py module")
