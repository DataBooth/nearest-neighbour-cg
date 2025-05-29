FROM python:3.13-slim-bullseye

# Install build tools and dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    cmake \
    g++ \
    python3-dev \
    libboost-all-dev \
    pybind11-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install -U uv

WORKDIR /app

# Create a non-root user
RUN useradd -m appuser

# Copy dependency files first for cache
COPY pyproject.toml pyproject.toml

# Set up venv and install dependencies
RUN uv venv .venv
ENV VIRTUAL_ENV=/app/.venv
ENV PATH="/app/.venv/bin:$PATH"
RUN uv sync --no-dev

# Copy all source code and CMakeLists.txt
COPY . .

# Build C++ extensions (in /app/build)
RUN mkdir -p build && \
    cd build && \
    cmake -DPython3_EXECUTABLE=/app/.venv/bin/python .. && \
    make

# Fix permissions for appuser
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose Streamlit port
EXPOSE 8501

# Run Streamlit app
CMD sh -c 'streamlit run python/app/hulls.py --server.port=${PORT:-8501} --server.address=0.0.0.0'
