import sys

sys.path.insert(0, "build/")
import convex_hull_ext


def test_triangle():
    # Simple triangle: hull should be the triangle itself (closed polygon)
    points = [[0, 0], [1, 0], [0, 1]]
    hull = convex_hull_ext.compute_convex_hull(points)
    # The hull should contain all triangle points, order may vary
    assert len(hull) == 4  # 3 points + repeat of first for closed polygon
    for pt in points:
        assert pt in hull


def test_square_with_inner_point():
    # Square with a point inside: hull is the four corners
    points = [[0, 0], [1, 0], [1, 1], [0, 1], [0.5, 0.5]]
    hull = convex_hull_ext.compute_convex_hull(points)
    assert len(hull) == 5  # 4 corners + repeat of first
    corners = [[0, 0], [1, 0], [1, 1], [0, 1]]
    for corner in corners:
        assert corner in hull
    assert [0.5, 0.5] not in hull  # inner point should not be in hull


def test_colinear_points():
    # All points colinear: hull is endpoints (Boost may return all points)
    points = [[0, 0], [1, 1], [2, 2]]
    hull = convex_hull_ext.compute_convex_hull(points)
    assert len(hull) >= 2  # At least the two endpoints


def test_empty_input():
    # Empty input: hull should be empty
    hull = convex_hull_ext.compute_convex_hull([])
    assert hull == []


def test_duplicate_points():
    # Duplicate points: hull should be correct
    points = [[0, 0], [1, 0], [1, 1], [0, 1], [0, 0], [1, 1]]
    hull = convex_hull_ext.compute_convex_hull(points)
    corners = [[0, 0], [1, 0], [1, 1], [0, 1]]
    for corner in corners:
        assert corner in hull


# You can add more tests for edge cases as needed
