#define CATCH_CONFIG_MAIN
#include "catch.hpp"
#include "KDTree2D_CGAL.hpp"

TEST_CASE("KDTree2D_CGAL finds correct nearest neighbour", "[KDTree2D_CGAL]")
{
    std::vector<Point_2> points = {Point_2(0, 0), Point_2(2, 2), Point_2(10, 10)};
    KDTree2D_CGAL tree(points);

    SECTION("Query at (1,1) finds one of the two closest points")
    {
        auto [idx, dist] = tree.query(1, 1);
        REQUIRE((idx == 0 || idx == 1));
        REQUIRE(Approx(dist).margin(1e-8) == std::sqrt(2.0));
    }

    SECTION("Query at (10,10) finds the last point exactly")
    {
        auto [idx, dist] = tree.query(10, 10);
        REQUIRE(idx == 2);
        REQUIRE(Approx(dist).margin(1e-8) == 0.0);
    }

    SECTION("Query at (0,0) finds the first point exactly")
    {
        auto [idx, dist] = tree.query(0, 0);
        REQUIRE(idx == 0);
        REQUIRE(Approx(dist).margin(1e-8) == 0.0);
    }
}
