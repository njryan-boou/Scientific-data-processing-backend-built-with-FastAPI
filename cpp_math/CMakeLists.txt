cmake_minimum_required(VERSION 3.16)

project(cpp_math LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(pybind11 REQUIRED)

# C++ library
add_library(cpp_math STATIC
    src/Vector.cpp
    src/Matrix.cpp
)

target_include_directories(cpp_math
    PUBLIC
        ${CMAKE_CURRENT_SOURCE_DIR}/include
)

# Python extension module
pybind11_add_module(_matrix_engine
    bindings/bindings.cpp
)

target_link_libraries(_matrix_engine
    PRIVATE
        cpp_math
)

target_include_directories(_matrix_engine
    PRIVATE
        ${CMAKE_CURRENT_SOURCE_DIR}/include
)

# Demo executable
add_executable(vector_demo
    examples/vector_demo.cpp
)

target_link_libraries(vector_demo
    PRIVATE
        cpp_math
)

# Put the compiled .pyd next to your Python package
set_target_properties(_matrix_engine PROPERTIES
    LIBRARY_OUTPUT_DIRECTORY_DEBUG ${CMAKE_CURRENT_SOURCE_DIR}/matrix_engine
    LIBRARY_OUTPUT_DIRECTORY_RELEASE ${CMAKE_CURRENT_SOURCE_DIR}/matrix_engine
    RUNTIME_OUTPUT_DIRECTORY_DEBUG ${CMAKE_CURRENT_SOURCE_DIR}/matrix_engine
    RUNTIME_OUTPUT_DIRECTORY_RELEASE ${CMAKE_CURRENT_SOURCE_DIR}/matrix_engine
)

# Optional install command
install(TARGETS _matrix_engine
    LIBRARY DESTINATION matrix_engine
    RUNTIME DESTINATION matrix_engine
)