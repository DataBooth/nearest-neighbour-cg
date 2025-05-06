# Detect compiler: prefer g++, fallback to clang++
compiler := `if command -v g++ > /dev/null 2>&1; then echo g++; elif command -v clang++ > /dev/null 2>&1; then echo clang++; else echo ""; fi`

# Set build directory variable
build_dir := "build"

# Default recipe: lists all available recipes
default:
    @just --list


## C++ recipes

# Configure and build with CMake and Make
build:
    mkdir -p {{build_dir}}
    cd build && cmake -DPython3_EXECUTABLE="$(which python)" .. && make

# Clean build artifacts
clean:
    rm -rf {{build_dir}}


rebuild:
    just clean
    just build


compiler:
    @if [ -z "{{compiler}}" ]; then \
        echo "No C++ compiler found (g++ or clang++ required)"; exit 1; \
    else \
        version=$({{compiler}} --version | head -n 1); \
        echo "Using compiler: {{compiler}} - version: $version"; \
    fi

run:
   cd {{build_dir}} && ./nearest_neighbour


## Python recipes

app app_name="python/app/main.py":
   streamlit run {{app_name}}