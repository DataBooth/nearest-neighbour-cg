#define CATCH_CONFIG_MAIN
#include <catch2/catch_test_macros.hpp> // (v3.x style)

// Directly include the implementation file (since no header)
#include "../bindings/convex_hull_ext.cpp"

TEST_CASE("Convex hull of triangle", "[convex_hull]")
{
    std::vector<std::vector<double>> points = {{0, 0}, {1, 0}, {0, 1}};
    auto hull = compute_convex_hull(points);
    REQUIRE(hull.size() == 4); // 3 points + repeat of first
}

TEST_CASE("Convex hull of square with inner point", "[convex_hull]")
{
    std::vector<std::vector<double>> points = {{0, 0}, {1, 0}, {1, 1}, {0, 1}, {0.5, 0.5}};
    auto hull = compute_convex_hull(points);
    REQUIRE(hull.size() == 5); // 4 corners + repeat of first
}
