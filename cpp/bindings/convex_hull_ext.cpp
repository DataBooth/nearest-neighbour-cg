/**
 * @file convex_hull_ext.cpp
 * @brief Python extension for computing the convex hull of 2D points using Boost.Geometry.
 *
 * ## Overview
 * This module exposes a function to Python (`compute_convex_hull`) that computes the convex hull
 * of a set of 2D points. The convex hull is the smallest convex polygon that contains all the points.
 * The implementation leverages Boost.Geometry's efficient convex hull algorithm.
 *
 * ## Algorithm
 * The convex hull is computed using Boost.Geometry's `convex_hull` function, which implements
 * a variant of the Graham scan or Andrew's monotone chain algorithm under the hood (depending on the version).
 * The input points are first converted into Boost's `multi_point` structure, and the resulting hull
 * is returned as a sequence of points forming the polygon's outer boundary.
 *
 * ## Data Structures
 * - **Point**: Alias for `bg::model::d2::point_xy<double>`, representing a 2D point (x, y).
 * - **Polygon**: Alias for `bg::model::polygon<Point>`, representing a polygon as a sequence of points.
 * - **bg::model::multi_point<Point>**: A collection of 2D points.
 * - **std::vector<std::vector<double>>**: Used for interoperability with Python (list of [x, y] pairs).
 *
 * ## Usage (from Python)
 * ```
 * import convex_hull_ext
 * points = [, [1, [0.5, 0.5]]
 * hull = convex_hull_ext.compute_convex_hull(points)
 * ```
 */

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <boost/geometry.hpp>
#include <boost/geometry/geometries/point_xy.hpp>
#include <boost/geometry/geometries/polygon.hpp>
#include <boost/geometry/geometries/multi_point.hpp>
#include <vector>

namespace py = pybind11;
namespace bg = boost::geometry;

// Type alias for a 2D point with double precision
using Point = bg::model::d2::point_xy<double>;

// Type alias for a polygon composed of 2D points
using Polygon = bg::model::polygon<Point>;

/**
 * @brief Computes the convex hull of a set of 2D points.
 *
 * @param points A vector of points, where each point is a vector of two doubles: [x, y].
 * @return A vector of points representing the convex hull in counter-clockwise order.
 *
 * The function:
 * 1. Converts the input to Boost.Geometry's multi_point structure.
 * 2. Computes the convex hull using Boost.Geometry.
 * 3. Extracts the outer boundary of the hull polygon as a list of [x, y] pairs.
 */
std::vector<std::vector<double>> compute_convex_hull(const std::vector<std::vector<double>> &points)
{
    // Step 1: Convert input points to Boost.Geometry's multi_point structure
    bg::model::multi_point<Point> bg_points;
    for (const auto &pt : points)
        if (pt.size() >= 2)
            bg_points.emplace_back(pt[0], pt[1]);

    // Step 2: Compute the convex hull (result is a polygon)
    Polygon hull;
    bg::convex_hull(bg_points, hull);

    // Step 3: Extract the outer boundary of the hull as a list of [x, y] pairs
    std::vector<std::vector<double>> result;
    for (const auto &pt : hull.outer())
        result.push_back({bg::get<0>(pt), bg::get<1>(pt)});
    return result;
}

/**
 * @brief Pybind11 module definition.
 *
 * Exposes the `compute_convex_hull` function to Python.
 */
PYBIND11_MODULE(convex_hull_ext, m)
{
    m.doc() = "Convex hull computation using Boost.Geometry";
    m.def("compute_convex_hull", &compute_convex_hull, "Compute convex hull for a list of 2D points");
}
