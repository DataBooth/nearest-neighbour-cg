import sys
from typing import List

import numpy as np
import plotly.graph_objects as go

sys.path.insert(0, "build/")
import convex_hull_ext


def generate_random_points(num_points: int, seed: int = None) -> List[List[float]]:
    """
    Generate a list of random 2D points.

    Args:
        num_points: Number of points to generate.
        seed: Optional random seed for reproducibility.

    Returns:
        A list of [x, y] coordinate pairs.
    """
    if seed is not None:
        np.random.seed(seed)
    return np.random.rand(num_points, 2).tolist()


def compute_convex_hull(points: List[List[float]]) -> np.ndarray:
    """
    Compute the convex hull of a set of 2D points using the C++ extension.

    Args:
        points: List of [x, y] points.

    Returns:
        Numpy array of convex hull vertices as [[x1, y1], [x2, y2], ...].
    """
    hull = convex_hull_ext.compute_convex_hull(points)
    return np.array(hull)


def plot_convex_hull(points: List[List[float]], hull: np.ndarray) -> None:
    """
    Plot the set of points and their convex hull using Plotly.

    Args:
        points: List of [x, y] points.
        hull: Numpy array of convex hull vertices.
    """
    points_np = np.array(points)
    fig = go.Figure()

    # Plot all points
    fig.add_trace(
        go.Scatter(
            x=points_np[:, 0],
            y=points_np[:, 1],
            mode="markers",
            name="Points",
            marker=dict(size=4, opacity=0.7),
        )
    )

    # Plot convex hull (closed polygon)
    hull_x = np.append(hull[:, 0], hull[0, 0])
    hull_y = np.append(hull[:, 1], hull[0, 1])
    fig.add_trace(
        go.Scatter(
            x=hull_x,
            y=hull_y,
            mode="lines+markers",
            name="Convex Hull",
            line=dict(color="red", width=2),
            marker=dict(color="red", size=6),
        )
    )

    fig.update_layout(
        title="Convex Hull of Random Points (2D)",
        xaxis_title="X",
        yaxis_title="Y",
        legend=dict(x=0.01, y=0.99),
    )
    fig.show()


def main(num_points: int = 1000, seed: int = 42) -> None:
    """
    Main function to generate points, compute the convex hull, and plot the result.

    Args:
        num_points: Number of random points to generate.
        seed: Random seed for reproducibility.
    """
    points = generate_random_points(num_points, seed)
    try:
        hull = compute_convex_hull(points)
        plot_convex_hull(points, hull)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
