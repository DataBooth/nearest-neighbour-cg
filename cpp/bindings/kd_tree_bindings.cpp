#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "nanoflann.hpp"
#include <vector>
#include <cmath>

namespace py = pybind11;

#include <iostream>
#include <vector>
#include <nanoflann.hpp>
#include <cmath>
#include <random>
#include <iomanip> // For std::setw

// PointCloud class encapsulates the data and nanoflann adaptor interface
class PointCloud
{
public:
    struct Point
    {
        double x, y;
    };
    std::vector<Point> pts;

    PointCloud(const std::vector<Point> &points) : pts(points) {}

    // nanoflann interface
    inline size_t kdtree_get_point_count() const { return pts.size(); }

    inline double kdtree_get_pt(const size_t idx, const size_t dim) const
    {
        return (dim == 0) ? pts[idx].x : pts[idx].y;
    }

    // Optional bounding-box computation: return false to default
    template <class BBOX>
    bool kdtree_get_bbox(BBOX &) const { return false; }
};

// KDTree wrapper class for nearest neighbor search
class KDTree2D
{
public:
    using KDTree_t = nanoflann::KDTreeSingleIndexAdaptor<
        nanoflann::L2_Simple_Adaptor<double, PointCloud>,
        PointCloud,
        2 /* dimension */
        >;

    KDTree2D(const PointCloud &cloud)
        : cloud_(cloud), index_(2, cloud_, nanoflann::KDTreeSingleIndexAdaptorParams(10))
    {
        index_.buildIndex();
    }

    // Query nearest neighbor for a given point (x,y)
    std::pair<size_t, double> query(double x, double y) const
    {
        double query_pt[2] = {x, y};
        size_t ret_index = size_t(-1);
        double out_dist_sqr = 0.0;

        nanoflann::KNNResultSet<double> resultSet(1);
        resultSet.init(&ret_index, &out_dist_sqr);
        index_.findNeighbors(resultSet, query_pt, nanoflann::SearchParameters(10));

        return {ret_index, std::sqrt(out_dist_sqr)};
    }

private:
    const PointCloud &cloud_;
    KDTree_t index_;
};

PYBIND11_MODULE(kd_tree_cpp, m)
{
    py::class_<PointCloud::Point>(m, "Point")
        .def(py::init<double, double>())
        .def_readwrite("x", &PointCloud::Point::x)
        .def_readwrite("y", &PointCloud::Point::y);

    py::class_<PointCloud>(m, "PointCloud")
        .def(py::init<const std::vector<PointCloud::Point> &>());

    py::class_<KDTree2D>(m, "KDTree2D")
        .def(py::init<const PointCloud &>())
        .def("query", &KDTree2D::query);
}
