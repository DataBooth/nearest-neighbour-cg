# Convex Hull Example: Fast C++ Backend with Python Visualisation

This project demonstrates how to use **C++** (via `Boost.Python` and `Boost.Geometry`) for efficient computational geometry, and **Python** (with Plotly) for interactive visualisation.

______________________________________________________________________

## 1. Overview

- **Backend:** C++ code using Boost.Geometry and Boost.Python to compute the convex hull of a set of points.
- **Frontend:** Python script to generate points, call the C++ function, and visualise the result using Plotly.

______________________________________________________________________

## 2. Key Files

- `convex_hull_ext.cpp`   # C++ code with Boost.Python wrapper
- `convex_hull_ext.so`    # Compiled module
- `visualise_hull.py`     # Python script for visualisation

______________________________________________________________________

## 3. Prerequisites

- **C++ Compiler** (e.g., `g++`)
- **Python 3.x**
- **Boost Libraries** (Boost.Geometry, Boost.Python)
- **Plotly** (Python package)
- **numpy** (Python package)

______________________________________________________________________

## 4. Installation

### Install Dependencies

**On Ubuntu:**

```sh
sudo apt-get update
sudo apt-get install g++ python3-dev libboost-python-dev libboost-geometry-dev
uv add numpy plotly
```

**On MacOS (with Homebrew):**

```sh
brew install boost python3
uv add numpy plotly
```

______________________________________________________________________

## 5. Build the C++ Module

Compile the C++ code to create a Python-importable module:

```sh
g++ -I/usr/include/python3.x -I/path/to/boost \
    -shared -fPIC convex_hull_ext.cpp -lboost_python3x -lpython3.x -o convex_hull_ext.so
```

*Replace `/usr/include/python3.x` and `/path/to/boost` with your actual paths if needed.*

______________________________________________________________________

## 6. Example C++ Code

**convex_hull_ext.cpp:**

```cpp
#include 
#include 
#include 
#include 
#include 

namespace bg = boost::geometry;
typedef bg::model::d2::point_xy Point;
typedef bg::model::polygon Polygon;

std::vector> compute_convex_hull(const std::vector>& points) {
    std::vector bg_points;
    for (const auto& pt : points) bg_points.push_back(Point(pt[0], pt[1]));

    Polygon hull;
    bg::convex_hull(bg_points, hull);

    std::vector> result;
    for (const auto& pt : hull.outer()) {
        result.push_back({bg::get(pt), bg::get(pt)});
    }
    return result;
}

BOOST_PYTHON_MODULE(convex_hull_ext) {
    using namespace boost::python;
    def("compute_convex_hull", compute_convex_hull);
}
```

______________________________________________________________________

## 7. Python Visualisation Script

**visualize_hull.py:**

```python
import convex_hull_ext
import numpy as np
import plotly.graph_objects as go

# Generate random points
points = np.random.rand(1000, 2).tolist()

# Compute convex hull using C++ function
hull = convex_hull_ext.compute_convex_hull(points)
hull = np.array(hull)

# Plot all points and convex hull with Plotly
fig = go.Figure()

# Scatter plot of all points
fig.add_trace(go.Scatter(
    x=np.array(points)[:,0],
    y=np.array(points)[:,1],
    mode='markers',
    name='Points',
    marker=dict(size=4, opacity=0.7)
))

# Line plot of the convex hull (close the loop)
fig.add_trace(go.Scatter(
    x=np.append(hull[:,0], hull[0,0]),
    y=np.append(hull[:,1], hull[0,1]),
    mode='lines+markers',
    name='Convex Hull',
    line=dict(color='red', width=2),
    marker=dict(color='red', size=6)
))

fig.update_layout(
    title='Convex Hull of Random Points (2D)',
    xaxis_title='X',
    yaxis_title='Y'
)
fig.show()
```

______________________________________________________________________

## 8. Usage

1. **Build the C++ module** as described above.
1. **Run the Python script:**
   ```sh
   python visualise_hull.py
   ```
1. **View the interactive plot** in your browser.

______________________________________________________________________

## 9. Notes

- **Performance:** The C++ backend is much faster for large datasets, making it ideal for computational geometry tasks.
- **Extensibility:** You can extend this example to other geometric problems or visualisations.

______________________________________________________________________

## 10. Troubleshooting

- **Module not found:** Ensure `convex_hull_ext.so` is in the same directory as your Python script.
- **Boost/Python paths:** Adjust include and library paths in the compilation command if needed.

______________________________________________________________________

## 11. License

This example is provided under the Apache 2.0 License.

______________________________________________________________________

## Appendix: C++ Types and Data Structures in `convex_hull_ext.cpp`

This appendix provides a quick reference to the key types and data structures used in the convex hull C++ extension module.

______________________________________________________________________

### 1. **Boost.Geometry Types**

| Type | Description | Example Usage |
|--------------------------------------------|-----------------------------------------------------------------------------------------------------|--------------------------------|
| `bg::model::d2::point_xy` | 2D point with double-precision coordinates. | `Point pt(1.0, 2.0);` |
| `bg::model::polygon` | Polygon type defined by a sequence of 2D points (outer boundary, optionally holes). | `Polygon hull;` |

**Type Aliases Used in the Code:**

```cpp
namespace bg = boost::geometry;
typedef bg::model::d2::point_xy Point;
typedef bg::model::polygon Polygon;
```

______________________________________________________________________

### 2. **Standard Library Types**

| Type | Description | Example Usage |
|-----------------------------|--------------------------------------------------------------|-----------------------------|
| `std::vector` | Dynamic array of doubles (used for a single point `[x, y]`). | `std::vector pt;` |
| `std::vector` | Dynamic array of Boost.Geometry points. | `std::vector pts;` |
| `std::vector>` | Dynamic array of 2D points, each as `[x, y]`. | `std::vector> points;` |

______________________________________________________________________

### 3. **Python Interface Types (via Boost.Python)**

| Type | Description |
|-----------------------------------------------|---------------------------------------------------------------------------------------------------|
| `std::vector>` (input) | Used to receive a list of `[x, y]` points from Python. |
| `std::vector>` (output) | Used to return the convex hull as a list of `[x, y]` points to Python. |

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
|---------------------------------|-----------------------------------------------|--------------------------|
| `Point` (`bg::model::d2::point_xy`) | 2D point with x and y coordinates | List or tuple `[x, y]` |
| `Polygon` (`bg::model::polygon`) | Polygon (outer boundary of points) | List of `[x, y]` lists |
| `std::vector>` | Sequence of points (input/output interface) | List of `[x, y]` lists |

______________________________________________________________________

### 6. **Conversion Flow**

- **Python → C++:**\
  Python `List[List[float]]` → C++ `std::vector>` → C++ `std::vector`

- **C++ → Python:**\
  C++ `Polygon` → C++ `std::vector>` → Python `List[List[float]]`

______________________________________________________________________

### 7. **Boost.Python Module Declaration**

```cpp
BOOST_PYTHON_MODULE(convex_hull_ext) {
    using namespace boost::python;
    def("compute_convex_hull", compute_convex_hull);
}
```

- Exposes the C++ function to Python as `convex_hull_ext.compute_convex_hull`.
