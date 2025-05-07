import numpy as np
from sklearn.neighbors import KDTree


class PythonKDTree:
    """
    Standalone Python KDTree nearest neighbour backend for benchmarking.
    """

    def __init__(self, points: np.ndarray):
        """
        Args:
            points: (N, 2) numpy array of input points
        """
        self.points = points
        self.tree = KDTree(points)

    def query(self, point: np.ndarray) -> tuple:
        """
        Find nearest neighbour for a single query point.

        Args:
            point: (2,) numpy array

        Returns:
            (index, distance)
        """
        dist, ind = self.tree.query([point], k=1)
        return int(ind[0][0]), float(dist[0][0])

    def query_batch(self, queries: np.ndarray) -> list:
        """
        Find nearest neighbours for a batch of query points.

        Args:
            queries: (M, 2) numpy array

        Returns:
            List of (index, distance) tuples
        """
        dists, inds = self.tree.query(queries, k=1)
        return [(int(idx[0]), float(dist[0])) for idx, dist in zip(inds, dists)]


class DuckDBNearestNeighbour:
    """DuckDB VSS backend."""

    def __init__(self, points: np.ndarray):
        import duckdb

        self.points = points
        self.dim = points.shape[1]
        self.con = duckdb.connect(database=":memory:")
        self._setup_table()
        self._create_index()

    def _setup_table(self):
        self.con.execute(f"CREATE TABLE points (id INTEGER, vec FLOAT[{self.dim}])")
        data = [
            (i, [float(x) for x in self.points[i]]) for i in range(len(self.points))
        ]
        self.con.executemany("INSERT INTO points VALUES (?, ?)", data)

    def _create_index(self):
        self.con.execute("INSTALL vss")
        self.con.execute("LOAD vss")
        self.con.execute("CREATE INDEX idx_vec ON points USING HNSW(vec)")

    def query(self, point: np.ndarray):
        query_vec_str = f"ARRAY{[float(x) for x in point]}"
        sql = f"""
            SELECT id, array_distance(vec, {query_vec_str}::FLOAT[{self.dim}]) AS distance
            FROM points
            ORDER BY distance
            LIMIT 1
        """
        idx, dist = self.con.execute(sql).fetchone()
        return int(idx), float(dist)

    def query_parallel(self, queries: np.ndarray):
        return [self.query(q) for q in queries]
