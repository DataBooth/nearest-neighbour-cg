#pragma once

#include <vector>
#include <utility>
#include <cstddef> // for size_t

class CGALKDTree2D
{
public:
    CGALKDTree2D(const std::vector<std::pair<double, double>> &points);
    std::pair<size_t, double> query(double x, double y) const;

private:
    struct Impl;
    Impl *pimpl_;
};
