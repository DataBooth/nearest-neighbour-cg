import duckdb
import numpy as np
import pandas as pd
from loguru import logger


class DuckDBNearestNeighbour:
    """
    DuckDB-based nearest neighbour search using HNSW index.
    """

    def __init__(self, points: np.ndarray):
        """
        Args:
            points: numpy array of shape (n_points, dim)
        """
        self.points = points
        self.dim = self.points.shape[1]
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

    def query(self, query_point, k=1):
        """
        Args:
            query_point: iterable of floats (dim,)
            k: number of nearest neighbours to return
        Returns:
            List of (id, distance)
        """
        query_point = [float(x) for x in query_point]
        query_vec_str = f"ARRAY{query_point}"
        sql = f"""
            SELECT id, array_distance(vec, {query_vec_str}::FLOAT[{self.dim}]) AS distance
            FROM points
            ORDER BY distance
            LIMIT {k}
        """
        logger.debug(f"Executing SQL: {sql}")
        results = self.con.execute(sql).fetchall()
        return results


def main():
    n_points = 1000
    n_queries = 50
    dim = 2
    FIXED_SEED = 42
    np.random.seed(FIXED_SEED)

    points = np.random.uniform(0, 100, size=(n_points, dim))
    queries = np.random.uniform(0, 100, size=(n_queries, dim))

    nn = DuckDBNearestNeighbour(points)

    # Collect results for all queries
    results_data = []
    for i, q in enumerate(queries):
        neighbours = nn.query(q, k=1)
        for idx, dist in neighbours:
            results_data.append(
                {
                    "Query #": i + 1,
                    "Query X": q[0],
                    "Query Y": q[1],
                    "Neighbour Index": idx,
                    "Neighbour X": points[idx][0],
                    "Neighbour Y": points[idx][1],
                    "Distance": dist,
                }
            )

    # Output as a DataFrame
    df = pd.DataFrame(results_data)
    print(df.to_markdown(index=False))  # Pretty print in terminal


if __name__ == "__main__":
    main()
