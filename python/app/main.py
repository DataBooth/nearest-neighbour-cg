from multiprocessing import Pool

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from sklearn.neighbors import KDTree

FIXED_SEED = 42
README_TITLE = "# `nearest-neighbour-cg`"


def query_point_wrapper(args):
    instance, pt = args
    return instance.query(pt[0], pt[1])


class PointCloud:
    def __init__(self, points: np.ndarray):
        self.points = points


class KDTree2D:
    def __init__(self, point_cloud: PointCloud):
        self.tree = KDTree(point_cloud.points)

    def query(self, x, y):
        dist, ind = self.tree.query([[x, y]], k=1)
        return ind[0][0], dist[0][0]

    def query_parallel(self, query_points):
        with Pool() as pool:
            return pool.map(query_point_wrapper, [(self, pt) for pt in query_points])


class RandomPointGenerator:
    def __init__(self, seed: int):
        self.rng = np.random.default_rng(seed)

    def generate_rectangle(self, num_points, x_range, y_range):
        xs = self.rng.uniform(x_range[0], x_range[1], num_points)
        ys = self.rng.uniform(y_range[0], y_range[1], num_points)
        return np.column_stack((xs, ys))

    def generate_circle(self, num_points, center, radius):
        points = []
        while len(points) < num_points:
            x = self.rng.uniform(center[0] - radius, center[0] + radius)
            y = self.rng.uniform(center[1] - radius, center[1] + radius)
            if (x - center[0]) ** 2 + (y - center[1]) ** 2 <= radius**2:
                points.append([x, y])
        return np.array(points)


class NearestNeighbourApp:
    def __init__(self):
        self.seed = FIXED_SEED
        self.point_gen = RandomPointGenerator(self.seed)

    def run(self):
        st.title("Nearest Neighbour Search Demo")

        # Tabs for README and App
        tabs = st.tabs(["Demo App", "README"])
        with tabs[0]:
            self.run_app_tab()
        with tabs[1]:
            self.show_readme_tab()

    def run_app_tab(self):
        st.write(
            "This demo allows you to generate random points and perform nearest neighbour search using a KDTree."
        )

        st.sidebar.subheader("Visualisation Notes:")
        st.sidebar.write(
            "Blue points are the input points, red points are the query points, and (after performing the nearest neighbour search) the green lines indicate the nearest neighbours."
        )
        st.sidebar.markdown("---")

        # Sidebar controls
        st.sidebar.subheader("Generate Settings for random points")
        num_points = st.sidebar.slider("Number of input points", 100, 5000, 100, 100)
        num_queries = st.sidebar.slider("Number of query points", 10, 1000, 10)
        shape = st.sidebar.selectbox("Input points shape", ["Rectangle", "Circle"])
        x_min, x_max = st.sidebar.slider("X range", -100.0, 100.0, (-50.0, 50.0))
        y_min, y_max = st.sidebar.slider("Y range", -100.0, 100.0, (-50.0, 50.0))
        radius = st.sidebar.slider("Circle radius (if selected)", 1.0, 100.0, 40.0)
        backend = st.sidebar.radio("Select backend", ["Python", "C++"])

        # Regenerate points button
        if st.sidebar.button("Regenerate Points"):
            self.seed += 1
            self.point_gen = RandomPointGenerator(self.seed)
            st.session_state["nn_results"] = None  # Reset results
            st.rerun()

        # Generate points
        if shape == "Rectangle":
            points = self.point_gen.generate_rectangle(
                num_points, (x_min, x_max), (y_min, y_max)
            )
        else:
            center = ((x_min + x_max) / 2, (y_min + y_max) / 2)
            points = self.point_gen.generate_circle(num_points, center, radius)
        query_points = self.point_gen.generate_rectangle(
            num_queries, (x_min, x_max), (y_min, y_max)
        )
        cloud = PointCloud(points)

        # Run NN search button
        if "nn_results" not in st.session_state:
            st.session_state["nn_results"] = None

        if st.button("Run Nearest Neighbour Search"):
            if backend == "Python":
                kd = KDTree2D(cloud)
                results = kd.query_parallel(query_points)
            else:
                st.warning("C++ backend not implemented in this demo.")
                results = [(None, None)] * len(query_points)
            st.session_state["nn_results"] = results

        # Persistent plot container
        plot_container = st.container()

        # Show results table and plot after NN search, otherwise just plot points
        results = st.session_state["nn_results"]
        if results is not None:
            # Results table
            st.subheader("Results Table")
            results_data = []
            for i, (qp, res) in enumerate(zip(query_points, results)):
                idx, dist = res
                neighbour = points[idx] if idx is not None else (None, None)
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

        # Always plot, with or without NN lines
        self.plot(points, query_points, results, container=plot_container)
        if results is not None:
            st.toast("Nearest neighbour search completed.", icon="✅")
            st.write(
                "The lines indicate the nearest neighbour connections between query points and input points."
            )

            df = pd.DataFrame(results_data)
            st.dataframe(df, use_container_width=True)

    def plot(self, points, query_points, results=None, container=None):
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
                    if idx is not None:
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
                # title="Nearest Neighbour Visualisation",
                xaxis_title="X",
                yaxis_title="Y",
                width=700,
                height=700,
                legend=dict(yanchor="bottom", y=0.99, xanchor="right", x=0.01),
            )
            st.plotly_chart(fig)

    def show_readme_tab(self):
        try:
            with open("README.md", "r") as f:
                readme = f.read()
                readme = readme.replace(README_TITLE, "")
            st.markdown(readme, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Could not load README.md: {e}")


if __name__ == "__main__":
    app = NearestNeighbourApp()
    app.run()
