#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <boost/geometry.hpp>
#include <boost/geometry/geometries/point_xy.hpp>
#include <boost/geometry/geometries/polygon.hpp>
#include <boost/geometry/geometries/multi_point.hpp>
#include <vector>

namespace py = pybind11;
namespace bg = boost::geometry;
using Point = bg::model::d2::point_xy<double>;
using Polygon = bg::model::polygon<Point>;

std::vector<std::vector<double>> compute_convex_hull(const std::vector<std::vector<double>> &points)
{
    bg::model::multi_point<Point> bg_points;
    for (const auto &pt : points)
        if (pt.size() >= 2)
            bg_points.emplace_back(pt[0], pt[1]);

    Polygon hull;
    bg::convex_hull(bg_points, hull);

    std::vector<std::vector<double>> result;
    for (const auto &pt : hull.outer())
        result.push_back({bg::get<0>(pt), bg::get<1>(pt)});
    return result;
}

PYBIND11_MODULE(convex_hull_ext, m)
{
    m.doc() = "Convex hull computation using Boost.Geometry";
    m.def("compute_convex_hull", &compute_convex_hull, "Compute convex hull for a list of 2D points");
}
