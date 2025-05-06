# Nearest Neighbour Search (SQL Backend - `DuckDB`)

## What is Happening in the SQL Version?

This version demonstrates how to perform **nearest neighbour search** using [DuckDB](https://duckdb.org/) and its [VSS (Vector Similarity Search) extension](https://duckdb.org/docs/extensions/vss.html). Instead of using in-memory data structures or external libraries, all data (points and queries) are stored and queried directly in an in-memory DuckDB database.

- **Points** are stored as rows in a DuckDB table, with each point represented as a fixed-length vector column (`FLOAT` for 2D).
- The **HNSW index** (Hierarchical Navigable Small World graph) is built on this vector column, enabling fast approximate nearest neighbour queries.
- For each query point, a SQL statement is run to find the closest point(s) using the `array_distance` function, sorted by distance, and limited to the top result(s).
- Results are collected and displayed in a pandas DataFrame for easy inspection.

## Why DuckDB?

DuckDB is a modern, fast, and lightweight SQL OLAP database that supports:
- **In-memory operation** (no need for disk files unless you want them)
- **SQL-based analytics** (easy to express complex queries)
- **Vector Similarity Search (VSS)** via the HNSW index, making it possible to do nearest neighbour search natively in SQL
- **Integration with Python and pandas**, making it a great tool for data science and analytics workflows

**Benefits of using DuckDB for nearest neighbour search:**
- **SQL Expressiveness:** You can combine nearest neighbour search with other SQL analytics, filtering, or joins.
- **Scalability:** DuckDB can efficiently handle much larger datasets than you might comfortably fit in memory with pure Python.
- **Reproducibility:** The logic is transparent and portable-your nearest neighbour logic is just SQL, not hidden in code.

## How is this Different from the Python and C++ Approaches?

| Approach         | Backend         | Index Type   | Query Style | Performance         | Use Case                                   |
|------------------|----------------|--------------|-------------|---------------------|---------------------------------------------|
| **Python**       | `sklearn`      | KDTree       | In-memory   | Fast for small/medium, exact | Simple, prototyping, teaching         |
| **C++**          | pybind11 module| KDTree (nanoflann) | In-memory   | Very fast, exact    | High-performance, batch/production          |
| **DuckDB (SQL)** | DuckDB + VSS   | HNSW         | SQL query   | Fast, scalable, approximate | Data analytics, SQL workflows, large data   |

- **Python (scikit-learn):** Uses a KDTree in pure Python, good for smaller datasets, easy to use, but limited by the Python interpreter’s speed and memory.
- **C++ (nanoflann via pybind11):** Wraps a high-performance KDTree in C++, offering the fastest exact results for in-memory data, but requires C++ compilation and integration.
- **DuckDB (SQL):** Stores all data in a SQL table, builds a HNSW index for fast approximate nearest neighbour search, and leverages SQL for querying. This approach is scalable, easily integrates with analytics, and is ideal for combining nearest neighbour search with other SQL operations.

## Example Output

Results are shown as a DataFrame:

| Query # | Query X | Query Y | Neighbour Index | Neighbour X | Neighbour Y | Distance |
|---------|---------|---------|-----------------|-------------|-------------|----------|
| 1       | 37.45   | 95.07   | 19              | 36.63       | 63.64       | 31.45    |
| ...     | ...     | ...     | ...             | ...         | ...         | ...      |

## When to Use Each Approach

- **Python:** Quick prototyping, teaching, or when you need exact results and the dataset is small.
- **C++:** Maximum speed for large in-memory datasets, or when integrating with C++ codebases.
- **DuckDB (SQL):** When you want to combine nearest neighbour search with SQL analytics, work with larger datasets, or need a portable, reproducible workflow.

---

**In summary:**  

The DuckDB SQL version lets you do scalable, fast, and flexible nearest neighbour search using only SQL. It’s especially powerful when you want to combine nearest neighbour search with other data analytics, or when your workflow is already SQL-centric.
