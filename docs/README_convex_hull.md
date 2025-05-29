This project demonstrates how to use **C++** (via `Boost.Geometry`) for efficient computational geometry, and **Python** (with Plotly) for interactive visualisation computing the convex hull in 2D for various distributions of points.

## What the hull?

A [**convex hull**](https://en.wikipedia.org/wiki/Convex_hull) is the smallest convex set that contains a given set of points in a space. In other words, it is the minimal convex boundary that completely encloses all the points. Convex means that, for any two points inside the shape, the straight line segment connecting them is also entirely inside the shape.

More formally, the convex hull of a set $X$ can be defined in several equivalent ways:

- It is the intersection of all convex sets containing $X$.
- It is the set of all convex combinations of points in $X$.
- For a finite set of points in the plane, you can imagine stretching a rubber band around the outside of the points; when released, the band forms the convex hull.

In two dimensions, the convex hull is a polygon whose vertices are a subset of the input points, and whose interior contains all the points. In three dimensions, it is the smallest convex polyhedron enclosing the points.

## Features

- Efficient 2D convex hull computation using C++ and `Boost.Geometry`.
- Python interface via [`pybind11`](https://pybind11.readthedocs.io).
- Interactive low-code [Streamlit](https://streamlit.io) app for visualising convex hulls of random point distributions.
- Cross-platform build with `CMake`.

______________________________________________________________________

## 1. Overview

- **Backend:** C++ code using `Boost.Geometry` and `pybind11` to compute the convex hull of a set of points.
- **Frontend:** Python script to generate points, call the C++ function, and visualise the result using Plotly within a Streamlit app.

______________________________________________________________________

## 2. Key Files

- `convex_hull_ext.cpp` # C++ code with `pybind11` wrapper
- `convex_hull_ext.so` # Compiled module
- `hulls.py` # Streamlit UI for visualisation

______________________________________________________________________

## 3. Prerequisites

- **C++ Compiler** (e.g., `g++`)
- **Python 3.x**
- **Boost Libraries** (`Boost.Geometry`)`and`pybind11\`.
- **Plotly** (Python package)
- **Streamlit** (Python package)

______________________________________________________________________

## 4. Installation

### Install Dependencies

**On MacOS (with Homebrew):**

```sh
brew install boost python3
uv add numpy plotly streamlit
```

______________________________________________________________________

## 5. Build the C++ Module

Compile the C++ code to create a Python-importable module using `CMake`. See `justfile` for build recipe.

______________________________________________________________________

## 6. Usage

1. **Build the C++ module** as described above.
1. **Run the Python script:**
   ```sh
   streamlit run python/app/hulls.py
   ```
1. **View the interactive plot** in your browser.

Great point! If the **number of points is set by a slider** in your Streamlit app, you should reflect that in your README/documentation. Here’s an updated section that makes it clear:

---

## 7. Distributions Used in This App

This app demonstrates and visualises three types of 2D point distributions. You can control the **number of points** generated using a slider in the sidebar, allowing you to see how algorithms behave with different dataset sizes.

---

### A. Uniform Distribution

- **Description:** Points are spread evenly within a square region.
- **Parameters:**
  - **Region:** Square with x and y in 
  - **Number of points:** *Set by slider* (default: 200)
- **Properties:** Every location within the square has an equal chance of containing a point. Useful for simulating unbiased random sampling.

---

### B. Gaussian (Normal) Distribution

- **Description:** Points are clustered around a central mean, with density decreasing outward.
- **Parameters:**
  - **Mean (center):** (0.5, 0.5)
  - **Standard deviation:** 0.12 (for both x and y)
  - **Number of points:** *Set by slider* (default: 200)
- **Properties:** Most points are near the center, with fewer points farther away. Models natural clustering and randomness around an average.

---

### C. Clustered Distribution

- **Description:** Points are grouped into several tight clusters, each with its own center.
- **Parameters:**
  - **Number of clusters:** 4
  - **Cluster centers:** Randomly placed within [0.2, 0.8] for both x and y
  - **Cluster standard deviation:** 0.04
  - **Number of points:** *Set by slider* (default: 200, divided evenly among clusters)
- **Properties:** Points form several dense "islands" or clusters, simulating real-world scenarios like cities on a map or hotspots in data.

---

**How to use:**  
Use the sidebar to select a distribution and adjust the number of points with the slider. The app will generate and display a new set of points, letting you observe how geometric algorithms perform on different data layouts and sizes.

______________________________________________________________________

## 8. Notes

- **Performance:** The C++ backend is much faster for large datasets, making it ideal for computational geometry tasks.
- **Extensibility:** You can extend this example to other geometric problems or visualisations.

______________________________________________________________________

## 9. Troubleshooting

- **Module not found:** Ensure `convex_hull_ext.so` is in the same directory as your Python script.
- **Boost/Python paths:** Adjust include and library paths in the compilation command if needed.

______________________________________________________________________

## 10. License

This example is provided under the Apache 2.0 License.

______________________________________________________________________

## Appendix: C++ Types and Data Structures in `convex_hull_ext.cpp`

This appendix provides a quick reference to the key types and data structures used in the convex hull C++ extension module, now using **`pybind11`** for Python bindings.

______________________________________________________________________

### 1. **`Boost.Geometry` Types**

| Type | Description | Example Usage |
|----------------------------|------------------------------------------------------------------------------------------|-----------------------|
| `bg::model::d2::point_xy` | 2D point with double-precision coordinates. | `Point pt(1.0, 2.0);` |
| `bg::model::polygon` | Polygon type defined by a sequence of 2D points (outer boundary, optionally holes). | `Polygon hull;` |

**Type Aliases Used in the Code:**

```cpp
namespace bg = boost::geometry;
using Point = bg::model::d2::point_xy;
using Polygon = bg::model::polygon;
```

______________________________________________________________________

### 2. **Standard Library Types**

| Type | Description | Example Usage |
|-------------------------------------- |----------------------------------------------------|-------------------------------|
| `std::vector` | Dynamic array of doubles (used for a single point `[x, y]`). | `std::vector pt;` |
| `std::vector` | Dynamic array of Boost.Geometry points. | `std::vector pts;` |
| `std::vector>` | Dynamic array of 2D points, each as `[x, y]`. | `std::vector> points;` |

______________________________________________________________________

### 3. **Python Interface Types (via `pybind11`)**

| Type | Description |
|-----------------------------|-----------------------------------------------------------------------------|
| `std::vector>` (input) | Receives a list of `[x, y]` points from Python (list of lists). |
| `std::vector>` (output) | Returns the convex hull as a list of `[x, y]` points to Python. |

- `pybind11` automatically converts between Python lists-of-lists and these C++ types.

______________________________________________________________________

### 4. **Function Signatures**

```cpp
std::vector> compute_convex_hull(
    const std::vector>& points
);
```

- **Input:** List of points, each as `[x, y]` (from Python).
- **Output:** Convex hull vertices, each as `[x, y]` (to Python).

______________________________________________________________________

### 5. **Summary Table**

| C++ Type / Alias | Purpose / Description | Python Equivalent |
|-----------------------------------|------------------------------------------|-------------------------|
| `Point` (`bg::model::d2::point_xy`) | 2D point with x and y coordinates | List or tuple `[x, y]` |
| `Polygon` (`bg::model::polygon`) | Polygon (outer boundary of points) | List of `[x, y]` lists |
| `std::vector>` | Sequence of points (input/output) | List of `[x, y]` lists |

______________________________________________________________________

### 6. **Conversion Flow**

- **Python → C++:**\
  Python `List[List[float]]` → C++ `std::vector>`
- **C++ → Python:**\
  C++ `std::vector>` → Python `List[List[float]]`

`pybind11` handles these conversions automatically, so you can pass and return nested lists without custom converters.

______________________________________________________________________

### 7. **`pybind11` Module Declaration**

```cpp
#include 
#include 

PYBIND11_MODULE(convex_hull_ext, m) {
    m.def("compute_convex_hull", &compute_convex_hull, "Compute the convex hull of a set of 2D points");
}
```

- Exposes the C++ function to Python as `convex_hull_ext.compute_convex_hull`.

______________________________________________________________________

**Note:**

- All Python-C++ integration is handled by `pybind11` for simplicity, modern C++ compatibility, and robust type conversion.