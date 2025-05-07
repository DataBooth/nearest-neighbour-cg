import numpy as np
from sklearn.neighbors import KDTree


class PythonKDTreeBackend:
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
