import time
import numpy as np
import pandas as pd
from sklearn.neighbors import KDTree
from loguru import logger

# Import your C++ backends if available
try:
    from kd_tree_cpp import KDTree2D_CPP  # Replace with your actual import

    cpp_nanoflann_available = True
except ImportError:
    cpp_nanoflann_available = False

try:
    from cgal_bindings import KDTree2D_CGAL  # Replace with your actual import

    cpp_cgal_available = True
except ImportError:
    cpp_cgal_available = False

try:
    import duckdb
    from duckdb_nn import DuckDBNearestNeighbour  # Replace with your actual import

    duckdb_available = True
except ImportError:
    duckdb_available = False


# Python KDTree wrapper
class KDTree2D_Python:
    def __init__(self, points):
        self.points = points
        self.tree = KDTree(points)

    def query(self, point):
        dist, ind = self.tree.query([point], k=1)
        return ind[0][0], dist[0][0]


# Helper function to run a backend on all queries and time it
def run_backend(backend, queries, backend_name):
    logger.info(f"Running backend: {backend_name} on {len(queries)} queries.")
    start = time.perf_counter()
    results = [backend.query(q) for q in queries]
    end = time.perf_counter()
    logger.info(f"Backend {backend_name} completed in {end - start:.4f} seconds.")
    return results, end - start


def compare_results(results_dict, threshold=1e-6):
    """
    results_dict: {backend_name: [(idx, dist), ...]}
    Compares all backends pairwise and reports differences in index or distance > threshold.
    """
    backends = list(results_dict.keys())
    n_queries = len(next(iter(results_dict.values())))
    diffs = []
    for i in range(n_queries):
        # Gather ith result from each backend
        res_i = {b: results_dict[b][i] for b in backends}
        # Compare indices pairwise
        indices = [res_i[b][0] for b in backends]
        distances = [res_i[b][1] for b in backends]
        # Check if all indices match
        if len(set(indices)) > 1:
            diffs.append(
                {
                    "query_idx": i,
                    "type": "index_mismatch",
                    "indices": indices,
                    "distances": distances,
                }
            )
        else:
            # Indices match, check distance differences
            max_dist = max(distances)
            min_dist = min(distances)
            if max_dist - min_dist > threshold:
                diffs.append(
                    {
                        "query_idx": i,
                        "type": "distance_diff",
                        "indices": indices,
                        "distances": distances,
                        "diff": max_dist - min_dist,
                    }
                )
    logger.info(
        f"Compared results: found {len(diffs)} differences exceeding threshold {threshold}."
    )
    return diffs


def main():
    logger.add("nn_benchmark.log", rotation="10 MB")
    np.random.seed(42)
    Npointexp_max = 4  # Up to 10^4 points, adjust as needed
    threshold = 1e-6

    backends = {}

    # Prepare backend availability
    backends["Python KDTree"] = None
    if cpp_nanoflann_available:
        backends["C++ nanoflann"] = None
    if cpp_cgal_available:
        backends["C++ CGAL"] = None
    if duckdb_available:
        backends["DuckDB SQL"] = None

    report_rows = []

    for exp in range(1, Npointexp_max + 1):
        n_points = 10**exp
        n_queries = max(1, n_points // 10)
        logger.info(f"Scenario: {n_points} points, {n_queries} queries.")

        # Generate points and queries
        points = np.random.uniform(0, 100, size=(n_points, 2))
        queries = np.random.uniform(0, 100, size=(n_queries, 2))
        logger.info(f"Generated random points and queries for scenario.")

        # Initialize backends
        backends_instances = {}
        logger.info("Initializing backends...")
        backends_instances["Python KDTree"] = KDTree2D_Python(points)
        if cpp_nanoflann_available:
            backends_instances["C++ nanoflann"] = KDTree2D_CPP(points)
        if cpp_cgal_available:
            backends_instances["C++ CGAL"] = KDTree2D_CGAL(points)
        if duckdb_available:
            backends_instances["DuckDB SQL"] = DuckDBNearestNeighbour(points)
        logger.info(f"Backends initialized: {list(backends_instances.keys())}")

        # Run all backends
        results = {}
        times = {}
        for name, instance in backends_instances.items():
            res, t = run_backend(instance, queries, name)
            results[name] = res
            times[name] = t

        # Compare results
        diffs = compare_results(results, threshold=threshold)

        # Prepare report rows
        for name, t in times.items():
            report_rows.append(
                {
                    "Backend": name,
                    "Num Points": n_points,
                    "Num Queries": n_queries,
                    "Time (s)": t,
                    "Differences": len(diffs),
                }
            )

        # Optionally print some diff details
        if diffs:
            logger.warning(f"Sample differences for scenario {n_points} points:")
            for d in diffs[:5]:
                logger.warning(d)

    # Summary report
    df_report = pd.DataFrame(report_rows)
    logger.info("Benchmark complete. Summary report:")
    logger.info(f"\n{df_report}")

    # Save report CSV if desired
    df_report.to_csv("nn_comparison_report.csv", index=False)
    logger.info("Report saved as nn_comparison_report.csv.")


if __name__ == "__main__":
    main()
