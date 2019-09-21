cmake_minimum_required(VERSION 2.8.9)

set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/bin)
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/lib)

set(CMAKE_CXX_FLAGS "-O3")
add_compile_options(-Wall -Wextra -pedantic -Werror)

project(AStar)

set(project_sources
  src/main.cpp
  src/Board.cpp
)


add_library(Board src/Board.cpp)
add_executable(AStar src/main.cpp)
target_link_libraries(AStar Board)