cmake_minimum_required(VERSION 3.15)
project(nearest_neighbour_demo)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Add include directories for your C++ code
include_directories(
    ${PROJECT_SOURCE_DIR}/cpp/include
    /opt/homebrew/include      # Homebrew Apple Silicon
)

# Add the executable
add_executable(nearest_neighbour
    cpp/src/nearest_neighbour.cpp
)

# --- Python/pybind11 Section ---
# If the user has not set Python3_EXECUTABLE, default to 'python3' in PATH.
if(NOT Python3_EXECUTABLE)
    find_program(Python3_EXECUTABLE NAMES python3 python)
endif()

find_package(Python3 COMPONENTS Interpreter Development REQUIRED)
find_package(pybind11 REQUIRED)

message(STATUS "Using Python3_EXECUTABLE: ${Python3_EXECUTABLE}")
message(STATUS "Using Python3_INCLUDE_DIRS: ${Python3_INCLUDE_DIRS}")

add_library(kd_tree_cpp MODULE
    cpp/bindings/kd_tree_bindings.cpp
    cpp/src/nearest_neighbour.cpp
)

target_include_directories(kd_tree_cpp PRIVATE
    cpp/include
    ${Python3_INCLUDE_DIRS}
)

target_link_libraries(kd_tree_cpp PRIVATE
    pybind11::module
    Python3::Python
)

set_target_properties(kd_tree_cpp PROPERTIES PREFIX "")

if(APPLE)
    set_target_properties(kd_tree_cpp PROPERTIES SUFFIX ".so")
endif()
