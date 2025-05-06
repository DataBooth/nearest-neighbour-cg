#pragma once
#include <CGAL/Simple_cartesian.h>
#include <CGAL/Search_traits_2.h>
#include <CGAL/Kd_tree.h>
#include <CGAL/Orthogonal_k_neighbor_search.h>
#include <vector>
#include <algorithm>
#include <cmath>

typedef CGAL::Simple_cartesian<double> Kernel;
typedef Kernel::Point_2 Point_2;
typedef CGAL::Search_traits_2<Kernel> Traits;
typedef CGAL::Kd_tree<Traits> Tree;
typedef CGAL::Orthogonal_k_neighbor_search<Traits> K_neighbor_search;

class KDTree2D_CGAL
{
public:
    KDTree2D_CGAL(const std::vector<Point_2> &points)
        : points_(points), tree_(points_.begin(), points_.end()) {}

    // Returns (index, distance)
    std::pair<size_t, double> query(double x, double y) const
    {
        Point_2 query_pt(x, y);
        K_neighbor_search search(tree_, query_pt, 1);
        auto it = search.begin();
        const Point_2 &nn = it->first;
        auto idx = std::distance(points_.begin(), std::find(points_.begin(), points_.end(), nn));
        double dist_val = std::sqrt(it->second);
        return {idx, dist_val};
    }

private:
    std::vector<Point_2> points_;
    Tree tree_;
};
