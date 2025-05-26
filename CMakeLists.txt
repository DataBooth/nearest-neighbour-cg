cmake_minimum_required(VERSION 3.15)
project(nearest_neighbour_demo)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Add include directories for your C++ code
include_directories(
    ${PROJECT_SOURCE_DIR}/cpp/include
    /opt/homebrew/include
)

# Add the executable for your main C++ app (if needed)
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
find_package(Boost REQUIRED)  # Only need Boost.Geometry, not Boost.Python

message(STATUS "Using Python3_EXECUTABLE: ${Python3_EXECUTABLE}")
message(STATUS "Using Python3_INCLUDE_DIRS: ${Python3_INCLUDE_DIRS}")

# --- KD Tree Pybind11 Extension ---
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

# --- Convex Hull Pybind11 Extension ---
add_library(convex_hull_ext MODULE
    cpp/bindings/convex_hull_ext.cpp
)

target_include_directories(convex_hull_ext PRIVATE
    cpp/include
    ${Python3_INCLUDE_DIRS}
    ${Boost_INCLUDE_DIRS}
)

target_link_libraries(convex_hull_ext PRIVATE
    pybind11::module
    Python3::Python
    ${Boost_LIBRARIES}
)

set_target_properties(convex_hull_ext PROPERTIES PREFIX "")

if(APPLE)
    set_target_properties(convex_hull_ext PROPERTIES SUFFIX ".so")
endif()

message(STATUS "Python3_INCLUDE_DIRS: ${Python3_INCLUDE_DIRS}")
