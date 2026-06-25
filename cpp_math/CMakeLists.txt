cmake_minimum_required(VERSION 3.16)

project(cpp_math LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
enable_testing()

set(PYBIND11_FINDPYTHON ON)
find_package(Python COMPONENTS Interpreter Development.Module REQUIRED)
find_package(pybind11 REQUIRED)

# Header-only C++ library
add_library(cpp_math INTERFACE)

target_include_directories(cpp_math
    INTERFACE
        ${CMAKE_CURRENT_SOURCE_DIR}/include
)

# Python extension module
pybind11_add_module(_matrix_engine
    python/bindings.cpp
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

function(add_cpp_math_test name source)
    add_executable(${name} ${source})
    target_link_libraries(${name}
        PRIVATE
            cpp_math
    )
    add_test(NAME ${name} COMMAND ${name})
endfunction()

add_cpp_math_test(test_vector_basics tests/cpp/test_vector_basics.cpp)
add_cpp_math_test(test_vector_logic tests/cpp/test_vector_logic.cpp)
add_cpp_math_test(test_matrix_basics tests/cpp/test_matrix_basics.cpp)
add_cpp_math_test(test_matrix_linalg tests/cpp/test_matrix_linalg.cpp)
add_cpp_math_test(test_matrix_logic tests/cpp/test_matrix_logic.cpp)
add_cpp_math_test(test_validation tests/cpp/test_validation.cpp)
add_cpp_math_test(test_templates tests/cpp/test_templates.cpp)

# Put the compiled .pyd next to your Python package
set_target_properties(_matrix_engine PROPERTIES
    LIBRARY_OUTPUT_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/matrix_engine
    LIBRARY_OUTPUT_DIRECTORY_DEBUG ${CMAKE_CURRENT_SOURCE_DIR}/matrix_engine
    LIBRARY_OUTPUT_DIRECTORY_RELEASE ${CMAKE_CURRENT_SOURCE_DIR}/matrix_engine
    RUNTIME_OUTPUT_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/matrix_engine
    RUNTIME_OUTPUT_DIRECTORY_DEBUG ${CMAKE_CURRENT_SOURCE_DIR}/matrix_engine
    RUNTIME_OUTPUT_DIRECTORY_RELEASE ${CMAKE_CURRENT_SOURCE_DIR}/matrix_engine
)

# Optional install command
install(TARGETS _matrix_engine
    LIBRARY DESTINATION matrix_engine
    RUNTIME DESTINATION matrix_engine
)
