cmake_minimum_required(VERSION 3.24)

project(test
  LANGUAGES Fortran C
)

list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/cmake")

add_subdirectory(src)
