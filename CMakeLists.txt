cmake_minimum_required(VERSION 2.8.9)

set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/bin)
project(InsertionSort)

add_executable(InsertionSort src/ISort.cpp)
