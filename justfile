# Detect compiler: prefer g++, fallback to clang++
compiler := `if command -v g++ > /dev/null 2>&1; then echo g++; elif command -v clang++ > /dev/null 2>&1; then echo clang++; else echo ""; fi`

# Default recipe: lists all available recipes
default:
    @echo "Available recipes:"
    @just --list

build:
    @if [ -z "{{compiler}}" ]; then \
        echo "No C++ compiler found (g++ or clang++ required)"; exit 1; \
    else \
        echo "Using compiler: {{compiler}}"; \
        {{compiler}} -std=c++17 -O2 nearest_neighbor.cpp -o nearest_neighbor; \
    fi

compiler:
    @if [ -z "{{compiler}}" ]; then \
        echo "No C++ compiler found (g++ or clang++ required)"; exit 1; \
    else \
        echo "Using compiler: {{compiler}}"; \
    fi
run:
    ./nearest_neighbor

clean:
    rm -f nearest_neighbor