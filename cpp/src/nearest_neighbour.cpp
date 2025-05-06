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

int main()
{
    constexpr int num_points = 100;
    constexpr int num_queries = 50;

    // Generate 100 random points in [0, 100) x [0, 100)
    std::mt19937 rng(42); // Fixed seed for reproducibility
    std::uniform_real_distribution<double> dist(0.0, 100.0);

    std::vector<PointCloud::Point> points;
    for (int i = 0; i < num_points; ++i)
    {
        points.push_back({dist(rng), dist(rng)});
    }

    PointCloud cloud(points);
    KDTree2D tree(cloud);

    // Generate 50 random query points in [0, 100) x [0, 100)
    std::vector<PointCloud::Point> queries;
    for (int i = 0; i < num_queries; ++i)
    {
        queries.push_back({dist(rng), dist(rng)});
    }

    // Print table header
    std::cout << std::setw(6) << "Query#"
              << std::setw(12) << "QueryX"
              << std::setw(12) << "QueryY"
              << std::setw(8) << "Idx"
              << std::setw(12) << "NN_X"
              << std::setw(12) << "NN_Y"
              << std::setw(12) << "Dist" << '\n';

    // For each query, find nearest neighbor and print result
    for (int i = 0; i < num_queries; ++i)
    {
        const auto &q = queries[i];
        auto [idx, dist_val] = tree.query(q.x, q.y);
        const auto &nn = points[idx];
        std::cout << std::setw(6) << i + 1
                  << std::setw(12) << q.x
                  << std::setw(12) << q.y
                  << std::setw(8) << idx
                  << std::setw(12) << nn.x
                  << std::setw(12) << nn.y
                  << std::setw(12) << dist_val << '\n';
    }

    return 0;
}
