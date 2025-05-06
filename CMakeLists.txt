cmake_minimum_required(VERSION 3.10)
project(nearest_neighbour_demo)

# Set C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)


# Add include directories (adjust for nanoflann if needed)
include_directories(
    ${PROJECT_SOURCE_DIR}/cpp/include
    /opt/homebrew/include      # Homebrew Apple Silicon
)

# Add the executable
add_executable(nearest_neighbour
    cpp/src/nearest_neighbour.cpp
)

# If you have additional source files, add them here
# target_sources(nearest_neighbour PRIVATE cpp/src/other_file.cpp)
