#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "../include/Vector.hpp"
#include "../include/Matrix.hpp"
#include <sstream>
#include <utility>

namespace py = pybind11;

PYBIND11_MODULE(_matrix_engine, m)
{
	m.doc() = "Matrix/vector engine bindings";
	m.attr("__name__") = "_matrix_engine";
	m.attr("__doc__") = "Matrix/vector engine bindings for Python using pybind11";
	m.attr("__version__") = "1.0.0";
	m.attr("__author__") = "Noah Ryan";
	m.attr("__description__") = "A C++ library for matrix and vector operations, exposed to Python via pybind11.";
	py::class_<Vector>(m, "Vector")
    .def(py::init<size_t>())

	.def(py::init<const std::vector<double>&>())

    .def("size", &Vector::size)

	.def("__len__", &Vector::size)

    .def("__getitem__",[](const Vector& v, size_t i)
        {
            return v[i];
        }
    )

    .def("__setitem__",[](Vector& v, size_t i, double value)
        {
            v[i] = value;
        }
    )

    .def("__add__", &Vector::operator+)

    .def("__sub__", &Vector::operator-)

    .def("__mul__", static_cast<Vector (Vector::*)(const Vector&) const>(
            &Vector::operator*
        )
    )

    .def("__mul__", static_cast<Vector (Vector::*)(double) const>(
            &Vector::operator*
        )
    )

    .def("__truediv__", static_cast<Vector (Vector::*)(const Vector&) const>(
            &Vector::operator/
        )
    )

    .def("__truediv__", static_cast<Vector (Vector::*)(double) const>(
            &Vector::operator/
        )
    )

    .def("dot", &Vector::dot)

    .def("magnitude", &Vector::magnitude)

    .def("normalize", &Vector::normalize)

    .def("cross", &Vector::cross)

    .def("solve", &Vector::solve)

    .def("__repr__", [](const Vector& v)
        {
            std::ostringstream oss;
            oss << v;
            return oss.str();
        }
    );

	py::class_<Matrix>(m, "Matrix")

    .def(py::init<size_t, size_t>())

	.def(py::init<const std::vector<std::vector<double>>&>())

    .def_property_readonly("rows", &Matrix::getRows)
	.def_property_readonly("cols", &Matrix::getCols)

	.def_property_readonly("shape",
    [](const Matrix &m) {
        return py::make_tuple(m.getRows(), m.getCols());
    }
)

	.def("__len__", [](const Matrix& mat) {
		return mat.getRows();
	})

    .def("__getitem__", [](const Matrix& mat,
           std::pair<size_t, size_t> idx)
        {
            return mat(idx.first, idx.second);
        }
    )

    .def("__setitem__", [](Matrix& mat,
           std::pair<size_t, size_t> idx, double value)
        {
            mat(idx.first, idx.second) = value;
        }
    )

    .def("__add__", &Matrix::operator+)

    .def("__sub__", &Matrix::operator-)

    .def("__mul__",
        static_cast<Matrix (Matrix::*)(const Matrix&) const>(
            &Matrix::operator*
        )
    )

    .def("__mul__",
        static_cast<Matrix (Matrix::*)(double) const>(
            &Matrix::operator*
        )
    )

    .def("__truediv__",
        static_cast<Matrix (Matrix::*)(const Matrix&) const>(
            &Matrix::operator/
        )
    )

    .def("__truediv__",
        static_cast<Matrix (Matrix::*)(double) const>(
            &Matrix::operator/
        )
    )

    .def("matmul", &Matrix::matmul)

    .def("matvec", &Matrix::matvec)

    .def("vecmat", &Matrix::vecmat)

    .def("transpose", &Matrix::transpose)

    .def("determinant", &Matrix::determinant)

    .def("inverse", &Matrix::inverse)

    .def("adjugate", &Matrix::adjugate)

    .def("rref", &Matrix::rref)

    .def("rank", &Matrix::rank)

    .def("__repr__", [](const Matrix& mat)
        {
            std::ostringstream oss;
            oss << mat;
            return oss.str();
        }
    );

}
