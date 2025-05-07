import sys

sys.path.append("build")  # Add build dir to Python path

import kd_tree_cpp
import cgal_kdtree_cpp


# Nanoflan example usage:
points = [kd_tree_cpp.Point(x, y) for x, y in [(0.0, 0.0), (1.0, 1.0)]]
cloud = kd_tree_cpp.PointCloud(points)
tree = kd_tree_cpp.KDTree2D(cloud)
idx, dist = tree.query(1.1, 1.1)
print(idx, dist)

# CGAL example usage:
points = [(1.0, 2.0), (3.0, 4.0)]
tree = cgal_kdtree_cpp.CGALKDTree2D(points)
idx, dist = tree.query(1.5, 2.5)
