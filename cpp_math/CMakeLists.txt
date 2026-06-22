cmake_minimum_required(VERSION 3.16)

project(cpp_math LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_library(cpp_math
    src/Vector.cpp
    src/Matrix.cpp
)

target_include_directories(cpp_math
    PUBLIC
        ${CMAKE_CURRENT_SOURCE_DIR}/include
)

add_executable(vector_demo
    examples/vector_demo.cpp
)

target_link_libraries(vector_demo
    PRIVATE
        cpp_math
)