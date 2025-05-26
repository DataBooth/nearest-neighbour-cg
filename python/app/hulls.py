import sys

import numpy as np
import plotly.graph_objects as go
import streamlit as st
from pathlib import Path

sys.path.insert(0, "build/")
import convex_hull_ext


def display_markdown_file(
    filepath: str,
    remove_title: str = None,
    encoding: str = "utf-8",
    warn_if_missing: bool = True,
):
    path = Path(filepath)
    if path.exists():
        contents = path.read_text(encoding=encoding)
        if remove_title:
            contents = contents.replace(remove_title, "")
        st.markdown(contents)
    elif warn_if_missing:
        st.warning(f"{path.name} file not found in the project directory: {path}")


# --- Distribution options ---
def generate_points(num_points, distribution, seed=None):
    if seed is not None:
        np.random.seed(seed)
    if distribution == "Uniform":
        return np.random.rand(num_points, 2).tolist()
    elif distribution == "Normal":
        return np.random.randn(num_points, 2).tolist()
    elif distribution == "Clustered":
        # Example: 3 clusters
        centers = np.array([[0.2, 0.2], [0.8, 0.8], [0.5, 0.5]])
        points = []
        for _ in range(num_points):
            center = centers[np.random.choice(len(centers))]
            points.append((center + 0.07 * np.random.randn(2)).tolist())
        return points
    else:
        # Default to uniform
        return np.random.rand(num_points, 2).tolist()


def plot_convex_hull(points, hull):
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
    return fig


# --- Streamlit UI ---
st.title("Convex Hull Visualisation with Random Distributions")
st.subheader("Hull calculated via C++ code")


# Sidebar controls
num_points = st.sidebar.slider("Number of Points", 10, 2000, 500, step=10)
distribution = st.sidebar.selectbox("Distribution", ["Uniform", "Normal", "Clustered"])
seed = st.sidebar.slider("Random Seed", 0, 100, 42)


tab1, tab2 = st.tabs(["Visualisation", "Readme"])

with tab1:
    # Generate and compute
    points = generate_points(num_points, distribution, seed)
    try:
        hull = np.array(convex_hull_ext.compute_convex_hull(points))
        fig = plot_convex_hull(points, hull)
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error computing or plotting convex hull: {e}")

with tab2:
    display_markdown_file("docs/README_convex_hull.md")
