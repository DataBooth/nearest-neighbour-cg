import sys
import time
from typing import Any, List, Optional, Tuple

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from loguru import logger
from sklearn.neighbors import KDTree

# Try to import the C++ backend
sys.path.append("build")
try:
    import kd_tree_cpp
except ImportError:
    kd_tree_cpp = None

FIXED_SEED = 42
README_TITLE = "# `nearest-neighbour-cg`"

logger.add("nn_search.log", rotation="5 MB", enqueue=True, backtrace=True)


class PointCloud:
    """Encapsulates a set of 2D points."""

    def __init__(self, points: np.ndarray):
        """
        Args:
            points: Nx2 numpy array of (x, y) coordinates.
        """
        self.points = points


class KDTree2D:
    """Python KDTree wrapper using sklearn."""

    def __init__(self, point_cloud: PointCloud):
        """
        Args:
            point_cloud: PointCloud instance.
        """
        self.tree = KDTree(point_cloud.points)

    def query(self, x: float, y: float) -> Tuple[int, float]:
        """
        Find nearest neighbor for (x, y).
        Returns:
            Tuple of (index, distance)
        """
        dist, ind = self.tree.query([[x, y]], k=1)
        return int(ind[0][0]), float(dist[0][0])

    def query_parallel(self, query_points: np.ndarray) -> List[Tuple[int, float]]:
        """
        Query all points (serial, for Streamlit safety).
        Args:
            query_points: Nx2 numpy array.
        Returns:
            List of (index, distance) tuples.
        """
        return [self.query(pt[0], pt[1]) for pt in query_points]


class KDTree2D_CPP:
    """C++ KDTree wrapper using pybind11."""

    def __init__(self, point_cloud: PointCloud):
        """
        Args:
            point_cloud: PointCloud instance.
        Raises:
            ImportError: If C++ backend is unavailable.
        """
        if kd_tree_cpp is None:
            raise ImportError("C++ backend not available")
        points = [kd_tree_cpp.Point(float(x), float(y)) for x, y in point_cloud.points]
        self.cloud = kd_tree_cpp.PointCloud(points)
        self.tree = kd_tree_cpp.KDTree2D(self.cloud)

    def query(self, x: float, y: float) -> Tuple[int, float]:
        """
        Find nearest neighbor for (x, y) using C++ backend.
        Returns:
            Tuple of (index, distance)
        """
        idx, dist = self.tree.query(float(x), float(y))
        return int(idx), float(dist)

    def query_parallel(self, query_points: np.ndarray) -> List[Tuple[int, float]]:
        """
        Query all points (serial).
        Args:
            query_points: Nx2 numpy array.
        Returns:
            List of (index, distance) tuples.
        """
        return [self.query(pt[0], pt[1]) for pt in query_points]


class RandomPointGenerator:
    """Random point generator for rectangles and circles."""

    def __init__(self, seed: int):
        """
        Args:
            seed: Random seed.
        """
        self.rng = np.random.default_rng(seed)

    def generate_rectangle(
        self,
        num_points: int,
        x_range: Tuple[float, float],
        y_range: Tuple[float, float],
    ) -> np.ndarray:
        """
        Generate points in a rectangle.
        Returns:
            Nx2 numpy array.
        """
        xs = self.rng.uniform(x_range[0], x_range[1], num_points)
        ys = self.rng.uniform(y_range[0], y_range[1], num_points)
        return np.column_stack((xs, ys))

    def generate_circle(
        self, num_points: int, center: Tuple[float, float], radius: float
    ) -> np.ndarray:
        """
        Generate points in a circle.
        Returns:
            Nx2 numpy array.
        """
        points = []
        while len(points) < num_points:
            x = self.rng.uniform(center[0] - radius, center[0] + radius)
            y = self.rng.uniform(center[1] - radius, center[1] + radius)
            if (x - center[0]) ** 2 + (y - center[1]) ** 2 <= radius**2:
                points.append([x, y])
        return np.array(points)


class NearestNeighbourApp:
    """Main Streamlit app for nearest neighbour demo."""

    def __init__(self):
        """Initialise app state and sidebar."""
        self.seed = FIXED_SEED
        self.point_gen = RandomPointGenerator(self.seed)
        self.sidebar_state = self.create_sidebar()

    def create_sidebar(self) -> dict:
        """
        Create sidebar controls and return their values.
        Returns:
            Dictionary of sidebar parameters.
        """
        backend = st.sidebar.radio("Select backend", ["Python", "C++"])
        st.sidebar.markdown("---")

        st.sidebar.subheader("Visualisation Notes:")
        st.sidebar.write(
            "Blue points are the input points, red points are the query points, and (after performing the nearest neighbour search) the green lines indicate the nearest neighbours."
        )
        st.sidebar.markdown("---")
        if st.sidebar.button("Clear/Regenerate Points"):
            self.seed += 1
            self.point_gen = RandomPointGenerator(self.seed)
            st.session_state["nn_results"] = None
            st.rerun()
        st.sidebar.subheader("Generate Settings for random points")
        num_points = st.sidebar.slider("Number of input points", 100, 5000, 100, 100)
        num_queries = st.sidebar.slider("Number of query points", 10, 1000, 10)
        shape = st.sidebar.selectbox("Input points shape", ["Rectangle", "Circle"])
        x_min, x_max = st.sidebar.slider("X range", -100.0, 100.0, (-50.0, 50.0))
        y_min, y_max = st.sidebar.slider("Y range", -100.0, 100.0, (-50.0, 50.0))
        radius = st.sidebar.slider("Circle radius (if selected)", 1.0, 100.0, 40.0)

        return dict(
            backend=backend,
            num_points=num_points,
            num_queries=num_queries,
            shape=shape,
            x_min=x_min,
            x_max=x_max,
            y_min=y_min,
            y_max=y_max,
            radius=radius,
        )

    def generate_points(self) -> Tuple[np.ndarray, np.ndarray, PointCloud]:
        """
        Generate input and query points based on sidebar state.
        Returns:
            Tuple: (input points, query points, PointCloud)
        """
        s = self.sidebar_state
        if s["shape"] == "Rectangle":
            points = self.point_gen.generate_rectangle(
                s["num_points"], (s["x_min"], s["x_max"]), (s["y_min"], s["y_max"])
            )
        else:
            center = ((s["x_min"] + s["x_max"]) / 2, (s["y_min"] + s["y_max"]) / 2)
            points = self.point_gen.generate_circle(
                s["num_points"], center, s["radius"]
            )
        query_points = self.point_gen.generate_rectangle(
            s["num_queries"], (s["x_min"], s["x_max"]), (s["y_min"], s["y_max"])
        )
        cloud = PointCloud(points)
        return points, query_points, cloud

    def run(self) -> None:
        """Main entry point for the app."""

        st.title("Nearest Neighbour Search Demo")
        tabs = st.tabs(["Demo App", "README"])
        with tabs[0]:
            self.run_app_tab()
        with tabs[1]:
            self.show_readme_tab()

    def run_app_tab(self) -> None:
        """Run the main demo tab, including controls and results."""
        points, query_points, cloud = self.generate_points()
        s = self.sidebar_state
        if "nn_results" not in st.session_state:
            st.session_state["nn_results"] = None

        # Two columns: info text (left), run button (right)
        top_cols = st.columns([2, 1], gap="large")
        with top_cols[0]:
            st.write(
                "This demo allows you to generate random points and perform nearest neighbour search using a KDTree."
            )
        with top_cols[1]:
            if st.button("Run Nearest Neighbour Search"):
                logger.info(
                    f"Run started | num_points={s['num_points']}, num_queries={s['num_queries']}, "
                    f"shape={s['shape']}, x_range=({s['x_min']},{s['x_max']}), y_range=({s['y_min']},{s['y_max']}), "
                    f"radius={s['radius']}, backend={s['backend']}, seed={self.seed}"
                )
                t0 = time.perf_counter()
                if s["backend"] == "Python":
                    kd = KDTree2D(cloud)
                    results = kd.query_parallel(query_points)
                elif s["backend"] == "C++":
                    if kd_tree_cpp is None:
                        st.error("C++ backend is not available.")
                        results = [(None, None)] * len(query_points)
                    else:
                        kd = KDTree2D_CPP(cloud)
                        results = kd.query_parallel(query_points)
                else:
                    st.warning("Unknown backend selected.")
                    results = [(None, None)] * len(query_points)
                t1 = time.perf_counter()
                elapsed = t1 - t0
                logger.success(
                    f"Run completed | backend={s['backend']} | elapsed={elapsed:.4f}s"
                )
                st.session_state["nn_results"] = results
                st.toast(
                    f"Run completed in {elapsed:.4f} seconds using {s['backend']} backend.",
                    icon="✅",
                )

        plot_container = st.container(border=True)
        results = st.session_state["nn_results"]
        results_data = []
        if results is not None:
            st.subheader("Results Table")
            for i, (qp, res) in enumerate(zip(query_points, results)):
                idx, dist = res
                neighbour = (
                    points[idx]
                    if idx is not None and idx < len(points)
                    else (None, None)
                )
                results_data.append(
                    {
                        "Query #": i + 1,
                        "Query X": qp[0],
                        "Query Y": qp[1],
                        "NN Index": idx,
                        "NN X": neighbour[0],
                        "NN Y": neighbour[1],
                        "Distance": dist,
                    }
                )
        self.plot(points, query_points, results, container=plot_container)
        if results is not None:
            st.toast("Nearest neighbour search completed.", icon="✅")
            st.write(
                "The lines indicate the nearest neighbour connections between query points and input points."
            )
            df = pd.DataFrame(results_data)
            st.dataframe(df, use_container_width=True)

    def plot(
        self,
        points: np.ndarray,
        query_points: np.ndarray,
        results: Optional[List[Tuple[int, float]]] = None,
        container: Optional[Any] = None,
    ) -> None:
        """
        Plot points and nearest neighbour lines.
        Args:
            points: Nx2 array of input points.
            query_points: Mx2 array of query points.
            results: List of (index, distance) tuples or None.
            container: Streamlit container to plot in.
        """
        if container is None:
            container = st
        with container:
            fig = go.Figure()
            fig.add_trace(
                go.Scatter(
                    x=points[:, 0],
                    y=points[:, 1],
                    mode="markers",
                    marker=dict(color="blue", size=6),
                    name="Input Points",
                )
            )
            fig.add_trace(
                go.Scatter(
                    x=query_points[:, 0],
                    y=query_points[:, 1],
                    mode="markers",
                    marker=dict(color="red", size=8, symbol="x"),
                    name="Query Points",
                )
            )
            if results is not None:
                for (qx, qy), (idx, dist) in zip(query_points, results):
                    if idx is not None and idx < len(points):
                        nx, ny = points[idx]
                        fig.add_trace(
                            go.Scatter(
                                x=[qx, nx],
                                y=[qy, ny],
                                mode="lines",
                                line=dict(color="green", dash="dash"),
                                showlegend=False,
                            )
                        )
            fig.update_layout(
                xaxis_title="X",
                yaxis_title="Y",
                width=700,
                height=700,
                legend=dict(yanchor="bottom", y=0.99, xanchor="right", x=0.01),
            )
            st.plotly_chart(fig)

    def show_readme_tab(self) -> None:
        """Display README tab."""
        try:
            with open("README.md", "r") as f:
                readme = f.read()
                readme = readme.replace(README_TITLE, "")
            st.markdown(readme, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Could not load README.md: {e}")


if __name__ == "__main__":
    st.set_page_config(
        page_title="Nearest Neighbour Search Demo",
        page_icon="🌲",
        layout="wide",
    )
    app = NearestNeighbourApp()
    app.run()
