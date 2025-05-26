# This is a Justfile (https://just.systems/man/en/) for managing C++ and Python projects 
# with recipes for building, cleaning, and running applications.

# Detect compiler: prefer g++, fallback to clang++
compiler := `if command -v g++ > /dev/null 2>&1; then echo g++; elif command -v clang++ > /dev/null 2>&1; then echo clang++; else echo ""; fi`

# Set build directory variable
build_dir := "build"

# Set target executable name
target := "nearest_neighbour"

app_name := "python/app/main.py"

# Default recipe: lists all available recipes
default:
    @just --list


##  C++ recipes  ------------------------------------------------------


# Configure and build with CMake and Make (see CMakeLists.txt)
build:
    mkdir -p {{build_dir}}
    cd build && cmake -DPython3_EXECUTABLE="$(which python)" .. && make

# Clean build artifacts
clean:
    rm -rf {{build_dir}}


# Clean and (re)build the project
rebuild:
    just clean
    just build


# Check for C++ compiler / version
compiler:
    @if [ -z "{{compiler}}" ]; then \
        echo "No C++ compiler found (g++ or clang++ required)"; exit 1; \
    else \
        version=$({{compiler}} --version | head -n 1); \
        echo "Using compiler: {{compiler}} - version: $version"; \
    fi

# Run the target C++ application (within the build directory)
run:
   cd {{build_dir}} && ./{{target}}


##  Python recipes  ---------------------------------------------------

# NOTE: Use the uv package manager to install dependencies (see https://docs.astral.sh/uv/)

# Run the Streamlit app (within the Python virtual environment)
app:    
    #!/bin/bash
    if [ -z "$VIRTUAL_ENV" ]; then
        echo "Please activate the virtual environment first."
        echo "Run 'source .venv/bin/activate' to activate the virtual environment."
        echo ""
        exit 1
    fi

    if ! command -v streamlit >/dev/null 2>&1; then
        echo "Streamlit is not installed in the current environment."
        echo "Run 'uv add streamlit' after activating your virtual environment."
        exit 1
    fi

    streamlit run {{app_name}}


## ----- Convex Hull demo -------

# Build the convex hull extension
build-ch:
    g++ -I/usr/include/python3.x -I/usr/local/include/boost -shared -fPIC convex_hull_ext.cpp -lboost_python3x -lpython3.x -o convex_hull_ext.so