# Copyright (c) 2024, Henry Schreiner
# Developed under NSF AWARD OAC-2209877 and by the respective contributors.
# All rights reserved.
#
# SPDX-License-Identifier: Apache-2.0

if(CMAKE_VERSION VERSION_LESS 3.17)
  message(FATAL_ERROR "CMake 3.17+ required")
endif()

include_guard(DIRECTORY)

if(TARGET Python::NumPy)
  set(_Python Python)
elseif(TARGET Python3::NumPy)
  set(_Python Python3)
else()
  message(FATAL_ERROR "You must find Python or Python3 with the NumPy component before including F2PY!")
endif()

if(NOT DEFINED F2PY_INCLUDE_DIR)
  execute_process(
    COMMAND "${${_Python}_EXECUTABLE}" -c
            "import numpy.f2py; print(numpy.f2py.get_include())"
    OUTPUT_VARIABLE F2PY_inc_output
    ERROR_VARIABLE F2PY_inc_error
    RESULT_VARIABLE F2PY_inc_result
    OUTPUT_STRIP_TRAILING_WHITESPACE
    ERROR_STRIP_TRAILING_WHITESPACE)

  if(NOT F2PY_inc_result EQUAL 0)
    message(FATAL_ERROR "Can't find f2py, got ${F2PY_inc_output} ${F2PY_inc_error}")
  endif()

  set(F2PY_INCLUDE_DIR "${F2PY_inc_output}" CACHE STRING "")
  mark_as_advanced(F2PY_INCLUDE_DIR)
endif()

add_library(F2Py::Headers IMPORTED INTERFACE)
target_include_directories(F2Py::Headers INTERFACE "${F2PY_INCLUDE_DIR}")

function(f2py_object_library NAME TYPE)
  add_library(${NAME} ${TYPE} "${F2PY_INCLUDE_DIR}/fortranobject.c")
  target_link_libraries(${NAME} PUBLIC ${_Python}::NumPy F2Py::Headers)
  if("${TYPE}" STREQUAL "OBJECT")
    set_property(TARGET ${NAME} PROPERTY POSITION_INDEPENDENT_CODE ON)
  endif()
endfunction()

function(f2py_generate_signature MODULE)
  cmake_parse_arguments(
    PARSE_ARGV 1
    F2PY
    "NOLOWER"
    "OUTPUT;OUTPUT_VARIABLE"
    "F2PY_ARGS;SKIP;ONLY"
  )
  set(ALL_FILES ${F2PY_UNPARSED_ARGUMENTS})

  if(NOT F2PY_OUTPUT)
    message(FATAL_ERROR "OUTPUT <signature.pyf> is required")
  endif()

  if(NOT ALL_FILES)
    message(FATAL_ERROR "One or more input files must be specified")
  endif()

  if(IS_ABSOLUTE "${F2PY_OUTPUT}")
    set(abs_pyf_file "${F2PY_OUTPUT}")
  else()
    set(abs_pyf_file "${CMAKE_CURRENT_BINARY_DIR}/${F2PY_OUTPUT}")
  endif()

  set(abs_source_files)
  foreach(file IN LISTS ALL_FILES)
    if(IS_ABSOLUTE "${file}")
      list(APPEND abs_source_files "${file}")
    else()
      list(APPEND abs_source_files "${CMAKE_CURRENT_SOURCE_DIR}/${file}")
    endif()
  endforeach()

  # Translate the ONLY/SKIP routine filters into f2py's "only: <names> :" /
  # "skip: <names> :" selector blocks (each runs until a bare ":").
  set(selectors)
  if(F2PY_ONLY)
    list(APPEND selectors "only:" ${F2PY_ONLY} ":")
  endif()
  if(F2PY_SKIP)
    list(APPEND selectors "skip:" ${F2PY_SKIP} ":")
  endif()

  if(F2PY_NOLOWER)
    set(lower "--no-lower")
  else()
    set(lower "--lower")
  endif()

  # --overwrite-signature is required: f2py refuses to replace an existing .pyf,
  # which would break incremental rebuilds.
  add_custom_command(
    OUTPUT "${abs_pyf_file}"
    DEPENDS ${abs_source_files}
    VERBATIM
    COMMAND
      "${${_Python}_EXECUTABLE}" -m numpy.f2py
      -h "${abs_pyf_file}" --overwrite-signature -m "${MODULE}"
      ${abs_source_files} ${selectors} ${lower} "${F2PY_F2PY_ARGS}"
    COMMAND_EXPAND_LISTS
    COMMENT
      "F2PY generating ${MODULE} signature"
  )

  set_source_files_properties("${abs_pyf_file}" PROPERTIES GENERATED TRUE)

  if(F2PY_OUTPUT_VARIABLE)
    set(${F2PY_OUTPUT_VARIABLE} "${abs_pyf_file}" PARENT_SCOPE)
  endif()
endfunction()

function(f2py_generate_module NAME)
  cmake_parse_arguments(
    PARSE_ARGV 1
    F2PY
    "NOLOWER;F77;F90"
    "OUTPUT_DIR;OUTPUT_VARIABLE"
    "F2PY_ARGS"
  )
  set(ALL_FILES ${F2PY_UNPARSED_ARGUMENTS})

  if(NOT ALL_FILES)
    message(FATAL_ERROR "One or more input files must be specified")
  endif()

  if(NOT F2PY_OUTPUT_DIR)
    set(F2PY_OUTPUT_DIR "${CMAKE_CURRENT_BINARY_DIR}")
  endif()

  set(abs_pyf_file)
  if(NAME MATCHES "\\.pyf$")
    if(IS_ABSOLUTE "${NAME}")
      set(abs_pyf_file "${NAME}")
    else()
      set(abs_pyf_file "${CMAKE_CURRENT_SOURCE_DIR}/${NAME}")
    endif()
    get_filename_component(NAME "${NAME}" NAME_WE)
  endif()

  if(F2PY_F77 AND F2PY_F90)
    message(FATAL_ERROR "Can't specify F77 and F90")
  elseif(NOT F2PY_F77 AND NOT F2PY_F90)
    set(HAS_F90_FILE FALSE)

    # Free-form Fortran (.f90 and later) generates a -f2pywrappers2.f90 wrapper;
    # fixed-form F77 (.f/.F) does not. Lowercase first so .F90, .F95, etc. match.
    foreach(file IN LISTS ALL_FILES)
        string(TOLOWER "${file}" file_lower)
        if("${file_lower}" MATCHES "\\.(f90|f95|f03|f08|f15|f18)$")
            set(HAS_F90_FILE TRUE)
            break()
        endif()
    endforeach()

    if(HAS_F90_FILE)
      set(F2PY_F90 ON)
    else()
      set(F2PY_F77 ON)
    endif()
  endif()

  if(F2PY_F77)
    set(wrapper_files ${NAME}-f2pywrappers.f)
  else()
    set(wrapper_files ${NAME}-f2pywrappers.f ${NAME}-f2pywrappers2.f90)
  endif()

  set(module_output "${F2PY_OUTPUT_DIR}/${NAME}module.c")
  set(abs_wrapper_files)
  foreach(wrapper IN LISTS wrapper_files)
    list(APPEND abs_wrapper_files "${F2PY_OUTPUT_DIR}/${wrapper}")
  endforeach()

  if(F2PY_NOLOWER)
    set(lower "--no-lower")
  else()
    set(lower "--lower")
  endif()

  set(abs_all_files)
  foreach(file IN LISTS ALL_FILES)
    if(IS_ABSOLUTE "${file}")
      list(APPEND abs_all_files "${file}")
    else()
      list(APPEND abs_all_files "${CMAKE_CURRENT_SOURCE_DIR}/${file}")
    endif()
  endforeach()

  # A signature file fully specifies the interface, so f2py reads only it; the
  # sources are compiled and linked separately (via OUTPUT_VARIABLE). Mixing the
  # two on the command line makes f2py reject the bare-subroutine source blocks.
  # Without a signature, f2py reads the sources directly to wrap module NAME.
  if(abs_pyf_file)
    set(f2py_inputs "${abs_pyf_file}")
  else()
    set(f2py_inputs ${abs_all_files} -m ${NAME})
  endif()

  add_custom_command(
    OUTPUT ${module_output} ${abs_wrapper_files}
    DEPENDS ${abs_all_files} ${abs_pyf_file}
    VERBATIM
    COMMAND
      "${${_Python}_EXECUTABLE}" -m numpy.f2py
      ${f2py_inputs} ${lower} "${F2PY_F2PY_ARGS}"
    COMMAND_EXPAND_LISTS
    COMMAND
      "${CMAKE_COMMAND}" -E touch ${abs_wrapper_files}
    WORKING_DIRECTORY "${F2PY_OUTPUT_DIR}"
    COMMENT
      "F2PY making ${NAME} wrappers"
  )

  # Include the original sources: they define the routines the generated
  # wrappers call. Omitting them only links on platforms that allow undefined
  # symbols in shared libraries (i.e. not Windows).
  if(F2PY_OUTPUT_VARIABLE)
    set(${F2PY_OUTPUT_VARIABLE} ${module_output} ${abs_wrapper_files} ${abs_all_files}
                                PARENT_SCOPE)
  endif()
endfunction()
