#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <CGAL/Simple_cartesian.h>
#include <CGAL/Search_traits_2.h>
#include <CGAL/Kd_tree.h>
#include <CGAL/Orthogonal_k_neighbor_search.h>
#include <vector>
#include <algorithm>
#include <cmath>

namespace py = pybind11;

typedef CGAL::Simple_cartesian<double> Kernel;
typedef Kernel::Point_2 Point_2;
typedef CGAL::Search_traits_2<Kernel> Traits;
typedef CGAL::Kd_tree<Traits> Tree;
typedef CGAL::Orthogonal_k_neighbor_search<Traits> K_neighbor_search;

class CGALKDTree2D
{
public:
    CGALKDTree2D(const std::vector<std::pair<double, double>> &points)
    {
        for (const auto &p : points)
        {
            pts_.emplace_back(p.first, p.second);
        }
        tree_ = std::make_unique<Tree>(pts_.begin(), pts_.end());
    }

    std::pair<size_t, double> query(double x, double y) const
    {
        Point_2 query_pt(x, y);
        K_neighbor_search search(*tree_, query_pt, 1);
        auto it = search.begin();
        const Point_2 &nn = it->first;
        // Find index in original vector
        auto idx = std::distance(pts_.begin(), std::find(pts_.begin(), pts_.end(), nn));
        double dist_val = std::sqrt(it->second);
        return {idx, dist_val};
    }

private:
    std::vector<Point_2> pts_;
    std::unique_ptr<Tree> tree_;
};

PYBIND11_MODULE(cgal_kdtree_cpp, m)
{
    py::class_<CGALKDTree2D>(m, "CGALKDTree2D")
        .def(py::init<const std::vector<std::pair<double, double>> &>())
        .def("query", &CGALKDTree2D::query);
}
