#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "nn_CGAL.cpp"
namespace py = pybind11;

PYBIND11_MODULE(nn_CGAL_cpp, m) {
    py::class_<CGALKDTree2D>(m, "CGALKDTree2D")
        .def(py::init<>())
        .def("CGALKDTree2D", &CGALKDTree2D::CGALKDTree2D, py::arg("std::vector<std::pair<double"), py::arg("&points"))
        .def("query", &CGALKDTree2D::query, py::arg("x"), py::arg("y"))
        .def("query_pt", &CGALKDTree2D::query_pt, py::arg("x"), py::arg("y"))
        .def("search", &CGALKDTree2D::search, py::arg("*tree_"), py::arg("query_pt"), py::arg("1"))
        ;
}