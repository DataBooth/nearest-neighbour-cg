#include <CGAL/Simple_cartesian.h>
#include <CGAL/Search_traits_2.h>
#include <CGAL/Kd_tree.h>
#include <CGAL/Orthogonal_k_neighbor_search.h>
#include <vector>
#include <iostream>
#include <random>
#include <iomanip>
#include <cmath>

typedef CGAL::Simple_cartesian<double> Kernel;
typedef Kernel::Point_2 Point_2;
typedef CGAL::Search_traits_2<Kernel> Traits;
typedef CGAL::Kd_tree<Traits> Tree;
typedef CGAL::Orthogonal_k_neighbor_search<Traits> K_neighbor_search;

int main()
{
    constexpr int num_points = 100;
    constexpr int num_queries = 50;

    // Generate random points in [0, 100) x [0, 100)
    std::mt19937 rng(42);
    std::uniform_real_distribution<double> dist(0.0, 100.0);

    std::vector<Point_2> points;
    for (int i = 0; i < num_points; ++i)
        points.emplace_back(dist(rng), dist(rng));

    Tree tree(points.begin(), points.end());

    // Generate random query points
    std::vector<Point_2> queries;
    for (int i = 0; i < num_queries; ++i)
        queries.emplace_back(dist(rng), dist(rng));

    // Print table header
    std::cout << std::setw(6) << "Query#"
              << std::setw(12) << "QueryX"
              << std::setw(12) << "QueryY"
              << std::setw(8) << "Idx"
              << std::setw(12) << "NN_X"
              << std::setw(12) << "NN_Y"
              << std::setw(12) << "Dist" << '\n';

    // For each query, find nearest neighbour and print result
    for (int i = 0; i < num_queries; ++i)
    {
        const Point_2 &q = queries[i];
        K_neighbor_search search(tree, q, 1);
        auto it = search.begin();
        const Point_2 &nn = it->first;
        // Find the index of the nearest neighbour in the original points vector
        auto idx = std::distance(points.begin(), std::find(points.begin(), points.end(), nn));
        double dist_val = std::sqrt(it->second); // CGAL returns squared distance

        std::cout << std::setw(6) << i + 1
                  << std::setw(12) << q.x()
                  << std::setw(12) << q.y()
                  << std::setw(8) << idx
                  << std::setw(12) << nn.x()
                  << std::setw(12) << nn.y()
                  << std::setw(12) << dist_val << '\n';
    }

    return 0;
}
