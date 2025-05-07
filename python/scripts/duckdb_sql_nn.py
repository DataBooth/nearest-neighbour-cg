import numpy as np
import pandas as pd

from src.kdtree_backends import DuckDBNearestNeighbour


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
