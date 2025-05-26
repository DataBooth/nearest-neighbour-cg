#include <boost/python.hpp>
#include <boost/geometry.hpp>
#include <boost/geometry/geometries/point_xy.hpp>
#include <boost/geometry/geometries/polygon.hpp>
#include <boost/geometry/geometries/multi_point.hpp>
#include <vector>

namespace bg = boost::geometry;
typedef bg::model::d2::point_xy<double> Point;
typedef bg::model::polygon<Point> Polygon;

std::vector<std::vector<double>> compute_convex_hull(const std::vector<std::vector<double>> &points)
{
    bg::model::multi_point<Point> bg_points;
    for (const auto &pt : points)
    // Ensure each point has at least two coordinates before constructing a 2D point
    // (defensive: avoids out-of-bounds access if input is malformed)
    {
        if (pt.size() >= 2)
            bg_points.emplace_back(pt[0], pt[1]);
    }

    Polygon hull;
    bg::convex_hull(bg_points, hull);

    std::vector<std::vector<double>> result;
    for (const auto &pt : hull.outer())
    {
        result.push_back({bg::get<0>(pt), bg::get<1>(pt)});
    }
    return result;
}

#include <boost/python.hpp>
BOOST_PYTHON_MODULE(convex_hull_ext)
{
    using namespace boost::python;
    def("compute_convex_hull", compute_convex_hull);
}