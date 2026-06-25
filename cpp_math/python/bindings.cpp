#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "../include/Vector.hpp"
#include "../include/Matrix.hpp"
#include "../include/exceptions.hpp"
#include "../include/validation.hpp"
#include <sstream>
#include <stdexcept>
#include <utility>

namespace py = pybind11;

namespace
{
PyObject* shape_error_type = nullptr;
PyObject* dimension_error_type = nullptr;
PyObject* index_error_type = nullptr;
PyObject* empty_matrix_error_type = nullptr;
PyObject* value_error_type = nullptr;

void translate_linalg_exception(std::exception_ptr p)
{
    if (!p) {
        return;
    }

    try {
        std::rethrow_exception(p);
    } catch (const linalg::ShapeError& e) {
        PyErr_SetString(shape_error_type, e.what());
    } catch (const linalg::DimensionError& e) {
        PyErr_SetString(dimension_error_type, e.what());
    } catch (const linalg::IndexError& e) {
        PyErr_SetString(index_error_type, e.what());
    } catch (const linalg::EmptyMatrixError& e) {
        PyErr_SetString(empty_matrix_error_type, e.what());
    } catch (const linalg::ValueError& e) {
        PyErr_SetString(value_error_type, e.what());
    } catch (const std::out_of_range& e) {
        PyErr_SetString(index_error_type, e.what());
    } catch (const std::invalid_argument& e) {
        PyErr_SetString(value_error_type, e.what());
    }
}
} // namespace

PYBIND11_MODULE(_matrix_engine, m)
{
    m.doc() = "Matrix/vector engine bindings";

    m.attr("__version__") = "1.1.0";
    m.attr("__author__") = "Noah Ryan";
    m.attr("__description__") = "C++ matrix engine";
    m.attr("__all__") = py::make_tuple(
        "Vector",
        "Matrix",
        "LinalgError",
        "ShapeError",
        "DimensionError",
        "IndexError",
        "EmptyMatrixError",
        "ValueError",
        "validation");

    auto linalg_error = py::register_exception<linalg::LinalgError>(
        m, "LinalgError", PyExc_RuntimeError);
    auto shape_error = py::register_exception<linalg::ShapeError>(
        m, "ShapeError", linalg_error.ptr());
    auto dimension_error = py::register_exception<linalg::DimensionError>(
        m, "DimensionError", linalg_error.ptr());
    auto index_error = py::register_exception<linalg::IndexError>(
        m, "IndexError", linalg_error.ptr());
    auto empty_matrix_error = py::register_exception<linalg::EmptyMatrixError>(
        m, "EmptyMatrixError", linalg_error.ptr());
    auto value_error = py::register_exception<linalg::ValueError>(
        m, "ValueError", linalg_error.ptr());

    shape_error_type = shape_error.ptr();
    dimension_error_type = dimension_error.ptr();
    index_error_type = index_error.ptr();
    empty_matrix_error_type = empty_matrix_error.ptr();
    value_error_type = value_error.ptr();

    py::register_exception_translator(&translate_linalg_exception);

    py::module_ validation = m.def_submodule(
        "validation",
        "Validation helpers used by the matrix/vector engine.");
    validation.def("require", &linalg::validate::require,
        py::arg("condition"), py::arg("message"),
        "Raise ValueError with message when condition is false.");
    validation.def("row", &linalg::validate::row,
        py::arg("index"), py::arg("rows"),
        "Validate that a row index is within [0, rows).");
    validation.def("column", &linalg::validate::column,
        py::arg("index"), py::arg("cols"),
        "Validate that a column index is within [0, cols).");
    validation.def("not_empty", &linalg::validate::not_empty<Matrix>,
        py::arg("matrix"),
        "Validate that a matrix has at least one row and one column.");
    validation.def("square", &linalg::validate::square<Matrix>,
        py::arg("matrix"),
        "Validate that a matrix has the same number of rows and columns.");
    validation.def("same_shape", &linalg::validate::same_shape<Matrix, Matrix>,
        py::arg("lhs"), py::arg("rhs"),
        "Validate that two matrices have identical shapes.");
    validation.def("multiplication", &linalg::validate::multiplication<Matrix, Matrix>,
        py::arg("lhs"), py::arg("rhs"),
        "Validate that two matrices are compatible for matrix multiplication.");
    validation.def("positive_dimension", &linalg::validate::positive_dimension,
        py::arg("value"), py::arg("name"),
        "Validate that a named dimension is greater than zero.");
    validation.def("reshape", &linalg::validate::reshape,
        py::arg("current"), py::arg("requested"),
        "Validate that a reshape preserves the total element count.");

    py::class_<Vector>(m, 
        "Vector",
        "A class representing a mathematical vector."
    )
    .def(py::init<size_t>(),
        py::arg("size"),
        "Create a zero-filled vector with size elements.")

	.def(py::init<const std::vector<double>&>(),
        py::arg("values"),
        "Create a vector from a sequence of numeric values.")

    .def("size", &Vector::size,
        "Return the number of elements in the vector.")

	.def("__len__", &Vector::size,
        "Return the number of elements in the vector.")

    .def("__iter__", [](Vector& v)
        {
            return py::make_iterator(v.begin(), v.end());
        },
        py::keep_alive<0, 1>(),
        "Iterate over vector values."
    )

    .def("__getitem__",[](const Vector& v, size_t i)
        {
            return v[i];
        },
        py::arg("index"),
        "Return the value at index."
    )

    .def("__setitem__",[](Vector& v, size_t i, double value)
        {
            v[i] = value;
        },
        py::arg("index"), py::arg("value"),
        "Set the value at index."
    )

    .def("__add__", &Vector::operator+,
        py::arg("other"),
        "Return the elementwise sum of two vectors.")

    .def("__radd__", [](const Vector& v, const Vector& other)
        {
            return other + v;
        },
        py::arg("other"),
        "Return the elementwise sum of two vectors."
    )

    .def("__sub__", &Vector::operator-,
        py::arg("other"),
        "Return the elementwise difference of two vectors.")

    .def("__rsub__", [](const Vector& v, const Vector& other)
        {
            return other - v;
        },
        py::arg("other"),
        "Return other minus this vector elementwise."
    )

    .def("__mul__", static_cast<Vector (Vector::*)(const Vector&) const>(
            &Vector::operator*
        )
        ,
        py::arg("other"),
        "Return the elementwise product of two vectors."
    )

    .def("__mul__", static_cast<Vector (Vector::*)(double) const>(
            &Vector::operator*
        )
        ,
        py::arg("scalar"),
        "Return this vector multiplied by a scalar."
    )

    .def("__rmul__", [](const Vector& v, const Vector& other)
        {
            return other * v;
        },
        py::arg("other"),
        "Return the elementwise product of two vectors."
    )

    .def("__rmul__", [](const Vector& v, double scalar)
        {
            return v * scalar;
        },
        py::arg("scalar"),
        "Return this vector multiplied by a scalar."
    )

    .def("__truediv__", static_cast<Vector (Vector::*)(const Vector&) const>(
            &Vector::operator/
        )
        ,
        py::arg("other"),
        "Return the elementwise quotient of two vectors."
    )

    .def("__truediv__", static_cast<Vector (Vector::*)(double) const>(
            &Vector::operator/
        )
        ,
        py::arg("scalar"),
        "Return this vector divided by a scalar."
    )

    .def("__rtruediv__", [](const Vector& v, const Vector& other)
        {
            return other / v;
        },
        py::arg("other"),
        "Return other divided by this vector elementwise."
    )

    .def("__rtruediv__", [](const Vector& v, double scalar)
        {
            Vector result(v.size());
            for (size_t i = 0; i < v.size(); ++i) {
                if (v[i] == 0.0) {
                    throw std::invalid_argument("Division by zero");
                }
                result[i] = scalar / v[i];
            }
            return result;
        },
        py::arg("scalar"),
        "Return scalar divided by this vector elementwise."
    )

    .def("__neg__", [](const Vector& v)
        {
            return v * -1.0;
        },
        "Return the negated vector."
    )

    .def("__eq__", [](const Vector& v, const Vector& other)
        {
            return v == other;
        },
        py::arg("other"),
        "Return an elementwise equality mask as a vector of 1.0 and 0.0."
    )

    .def("__ne__", [](const Vector& v, const Vector& other)
        {
            return v != other;
        },
        py::arg("other"),
        "Return an elementwise inequality mask as a vector of 1.0 and 0.0."
    )

    .def("__lt__", [](const Vector& v, const Vector& other)
        {
            return v < other;
        },
        py::arg("other"),
        "Return an elementwise less-than mask as a vector of 1.0 and 0.0."
    )

    .def("__le__", [](const Vector& v, const Vector& other)
        {
            return v <= other;
        },
        py::arg("other"),
        "Return an elementwise less-than-or-equal mask as a vector of 1.0 and 0.0."
    )

    .def("__gt__", [](const Vector& v, const Vector& other)
        {
            return v > other;
        },
        py::arg("other"),
        "Return an elementwise greater-than mask as a vector of 1.0 and 0.0."
    )

    .def("__ge__", [](const Vector& v, const Vector& other)
        {
            return v >= other;
        },
        py::arg("other"),
        "Return an elementwise greater-than-or-equal mask as a vector of 1.0 and 0.0."
    )

    .def("__and__", [](const Vector& v, const Vector& other)
        {
            return v & other;
        },
        py::arg("other"),
        "Return an elementwise logical-and mask as a vector of 1.0 and 0.0."
    )

    .def("__rand__", [](const Vector& v, const Vector& other)
        {
            return other & v;
        },
        py::arg("other"),
        "Return an elementwise logical-and mask as a vector of 1.0 and 0.0."
    )

    .def("__or__", [](const Vector& v, const Vector& other)
        {
            return v | other;
        },
        py::arg("other"),
        "Return an elementwise logical-or mask as a vector of 1.0 and 0.0."
    )

    .def("__ror__", [](const Vector& v, const Vector& other)
        {
            return other | v;
        },
        py::arg("other"),
        "Return an elementwise logical-or mask as a vector of 1.0 and 0.0."
    )

    .def("__xor__", [](const Vector& v, const Vector& other)
        {
            return v ^ other;
        },
        py::arg("other"),
        "Return an elementwise logical-xor mask as a vector of 1.0 and 0.0."
    )

    .def("__rxor__", [](const Vector& v, const Vector& other)
        {
            return other ^ v;
        },
        py::arg("other"),
        "Return an elementwise logical-xor mask as a vector of 1.0 and 0.0."
    )

    .def("__invert__", [](const Vector& v)
        {
            return !v;
        },
        "Return an elementwise logical-not mask as a vector of 1.0 and 0.0."
    )

    .def("__iadd__", [](Vector& v, const Vector& other) -> Vector&
        {
            v = v + other;
            return v;
        },
        py::return_value_policy::reference_internal,
        py::arg("other"),
        "Add another vector into this vector elementwise."
    )

    .def("__isub__", [](Vector& v, const Vector& other) -> Vector&
        {
            v = v - other;
            return v;
        },
        py::return_value_policy::reference_internal,
        py::arg("other"),
        "Subtract another vector from this vector elementwise."
    )

    .def("__imul__", [](Vector& v, const Vector& other) -> Vector&
        {
            v = v * other;
            return v;
        },
        py::return_value_policy::reference_internal,
        py::arg("other"),
        "Multiply this vector by another vector elementwise."
    )

    .def("__imul__", [](Vector& v, double scalar) -> Vector&
        {
            v = v * scalar;
            return v;
        },
        py::return_value_policy::reference_internal,
        py::arg("scalar"),
        "Multiply this vector by a scalar."
    )

    .def("__itruediv__", [](Vector& v, const Vector& other) -> Vector&
        {
            v = v / other;
            return v;
        },
        py::return_value_policy::reference_internal,
        py::arg("other"),
        "Divide this vector by another vector elementwise."
    )

    .def("__itruediv__", [](Vector& v, double scalar) -> Vector&
        {
            v = v / scalar;
            return v;
        },
        py::return_value_policy::reference_internal,
        py::arg("scalar"),
        "Divide this vector by a scalar."
    )

    .def("__matmul__", &Vector::dot,
        py::arg("other"),
        "Return the dot product when used as vector @ vector.")

    .def("__matmul__", [](const Vector& v, const Matrix& mat)
        {
            return mat.vecmat(v);
        },
        py::arg("matrix"),
        "Return vector-matrix multiplication when used as vector @ matrix."
    )

    .def("dot", &Vector::dot,
        py::arg("other"),
        "Return the dot product with another vector.")

    .def("magnitude", &Vector::magnitude,
        "Return the Euclidean magnitude of the vector.")

    .def("normalize", &Vector::normalize,
        "Return a normalized copy of the vector.")

    .def("cross", &Vector::cross,
        py::arg("other"),
        "Return the 3D cross product with another vector.")

    .def("solve", &Vector::solve,
        py::arg("A"),
        "Solve the linear system A*x = self. Currently not implemented.")

    .def("__repr__", [](const Vector& v)
        {
            std::ostringstream oss;
            oss << v;
            return oss.str();
        },
        "Return the string representation of the vector."
    )

    .def("__contains__", [](const Vector& v, double value)
        {
            for (size_t i = 0; i < v.size(); ++i) {
                if (v[i] == value) {
                    return true;
                }
            }
            return false;
        },
        py::arg("value"),
        "Return True if the vector contains value."
    );

    py::class_<Matrix>(m, 
        "Matrix",
        "A class representing a mathematical matrix."
    )

    .def(py::init<size_t, size_t>(),
        py::arg("rows"), py::arg("cols"),
        "Create a zero-filled matrix with the given row and column counts.")

	.def(py::init<const std::vector<std::vector<double>>&>(),
        py::arg("values"),
        "Create a matrix from a rectangular nested sequence of numeric values.")

    .def_property_readonly("rows", &Matrix::getRows,
        "Number of matrix rows.")
	.def_property_readonly("cols", &Matrix::getCols,
        "Number of matrix columns.")

	.def_property_readonly("shape",
    [](const Matrix &m) {
        return py::make_tuple(m.getRows(), m.getCols());
    },
        "Matrix shape as (rows, cols)."
)

	.def("__len__", [](const Matrix& mat) {
		return mat.getRows();
	},
        "Return the number of matrix rows.")

    .def("__iter__", [](const Matrix& mat)
        {
            py::list rows;
            for (size_t row = 0; row < mat.getRows(); ++row) {
                Vector values(mat.getCols());
                for (size_t col = 0; col < mat.getCols(); ++col) {
                    values[col] = mat(row, col);
                }
                rows.append(values);
            }
            return py::iter(rows);
        },
        "Iterate over matrix rows as Vector instances."
    )

    .def("__getitem__", [](const Matrix& mat,
           std::pair<size_t, size_t> idx)
        {
            return mat(idx.first, idx.second);
        },
        py::arg("index"),
        "Return the value at (row, column)."
    )

    .def("__setitem__", [](Matrix& mat,
           std::pair<size_t, size_t> idx, double value)
        {
            mat(idx.first, idx.second) = value;
        },
        py::arg("index"), py::arg("value"),
        "Set the value at (row, column)."
    )

    .def("__add__", &Matrix::operator+,
        py::arg("other"),
        "Return the elementwise sum of two matrices.")

    .def("__radd__", [](const Matrix& mat, const Matrix& other)
        {
            return other + mat;
        },
        py::arg("other"),
        "Return the elementwise sum of two matrices."
    )

    .def("__sub__", &Matrix::operator-,
        py::arg("other"),
        "Return the elementwise difference of two matrices.")

    .def("__rsub__", [](const Matrix& mat, const Matrix& other)
        {
            return other - mat;
        },
        py::arg("other"),
        "Return other minus this matrix elementwise."
    )

    .def("__mul__",
        static_cast<Matrix (Matrix::*)(const Matrix&) const>(
            &Matrix::operator*
        )
        ,
        py::arg("other"),
        "Return the elementwise product of two matrices."
    )

    .def("__mul__",
        static_cast<Matrix (Matrix::*)(double) const>(
            &Matrix::operator*
        )
        ,
        py::arg("scalar"),
        "Return this matrix multiplied by a scalar."
    )

    .def("__rmul__", [](const Matrix& mat, const Matrix& other)
        {
            return other * mat;
        },
        py::arg("other"),
        "Return the elementwise product of two matrices."
    )

    .def("__rmul__", [](const Matrix& mat, double scalar)
        {
            return mat * scalar;
        },
        py::arg("scalar"),
        "Return this matrix multiplied by a scalar."
    )

    .def("__truediv__",
        static_cast<Matrix (Matrix::*)(const Matrix&) const>(
            &Matrix::operator/
        )
        ,
        py::arg("other"),
        "Return the elementwise quotient of two matrices."
    )

    .def("__truediv__",
        static_cast<Matrix (Matrix::*)(double) const>(
            &Matrix::operator/
        )
        ,
        py::arg("scalar"),
        "Return this matrix divided by a scalar."
    )

    .def("__rtruediv__", [](const Matrix& mat, const Matrix& other)
        {
            return other / mat;
        },
        py::arg("other"),
        "Return other divided by this matrix elementwise."
    )

    .def("__rtruediv__", [](const Matrix& mat, double scalar)
        {
            Matrix result(mat.getRows(), mat.getCols());
            for (size_t row = 0; row < mat.getRows(); ++row) {
                for (size_t col = 0; col < mat.getCols(); ++col) {
                    if (mat(row, col) == 0.0) {
                        throw std::invalid_argument("Division by zero");
                    }
                    result(row, col) = scalar / mat(row, col);
                }
            }
            return result;
        },
        py::arg("scalar"),
        "Return scalar divided by this matrix elementwise."
    )

    .def("__neg__", [](const Matrix& mat)
        {
            return mat * -1.0;
        },
        "Return the negated matrix."
    )

    .def("__eq__", [](const Matrix& mat, const Matrix& other)
        {
            return mat == other;
        },
        py::arg("other"),
        "Return an elementwise equality mask as a matrix of 1.0 and 0.0."
    )

    .def("__ne__", [](const Matrix& mat, const Matrix& other)
        {
            return mat != other;
        },
        py::arg("other"),
        "Return an elementwise inequality mask as a matrix of 1.0 and 0.0."
    )

    .def("__lt__", [](const Matrix& mat, const Matrix& other)
        {
            return mat < other;
        },
        py::arg("other"),
        "Return an elementwise less-than mask as a matrix of 1.0 and 0.0."
    )

    .def("__le__", [](const Matrix& mat, const Matrix& other)
        {
            return mat <= other;
        },
        py::arg("other"),
        "Return an elementwise less-than-or-equal mask as a matrix of 1.0 and 0.0."
    )

    .def("__gt__", [](const Matrix& mat, const Matrix& other)
        {
            return mat > other;
        },
        py::arg("other"),
        "Return an elementwise greater-than mask as a matrix of 1.0 and 0.0."
    )

    .def("__ge__", [](const Matrix& mat, const Matrix& other)
        {
            return mat >= other;
        },
        py::arg("other"),
        "Return an elementwise greater-than-or-equal mask as a matrix of 1.0 and 0.0."
    )

    .def("__and__", [](const Matrix& mat, const Matrix& other)
        {
            return mat & other;
        },
        py::arg("other"),
        "Return an elementwise logical-and mask as a matrix of 1.0 and 0.0."
    )

    .def("__rand__", [](const Matrix& mat, const Matrix& other)
        {
            return other & mat;
        },
        py::arg("other"),
        "Return an elementwise logical-and mask as a matrix of 1.0 and 0.0."
    )

    .def("__or__", [](const Matrix& mat, const Matrix& other)
        {
            return mat | other;
        },
        py::arg("other"),
        "Return an elementwise logical-or mask as a matrix of 1.0 and 0.0."
    )

    .def("__ror__", [](const Matrix& mat, const Matrix& other)
        {
            return other | mat;
        },
        py::arg("other"),
        "Return an elementwise logical-or mask as a matrix of 1.0 and 0.0."
    )

    .def("__xor__", [](const Matrix& mat, const Matrix& other)
        {
            return mat ^ other;
        },
        py::arg("other"),
        "Return an elementwise logical-xor mask as a matrix of 1.0 and 0.0."
    )

    .def("__rxor__", [](const Matrix& mat, const Matrix& other)
        {
            return other ^ mat;
        },
        py::arg("other"),
        "Return an elementwise logical-xor mask as a matrix of 1.0 and 0.0."
    )

    .def("__invert__", [](const Matrix& mat)
        {
            return !mat;
        },
        "Return an elementwise logical-not mask as a matrix of 1.0 and 0.0."
    )

    .def("__iadd__", [](Matrix& mat, const Matrix& other) -> Matrix&
        {
            mat = mat + other;
            return mat;
        },
        py::return_value_policy::reference_internal,
        py::arg("other"),
        "Add another matrix into this matrix elementwise."
    )

    .def("__isub__", [](Matrix& mat, const Matrix& other) -> Matrix&
        {
            mat = mat - other;
            return mat;
        },
        py::return_value_policy::reference_internal,
        py::arg("other"),
        "Subtract another matrix from this matrix elementwise."
    )

    .def("__imul__", [](Matrix& mat, const Matrix& other) -> Matrix&
        {
            mat = mat * other;
            return mat;
        },
        py::return_value_policy::reference_internal,
        py::arg("other"),
        "Multiply this matrix by another matrix elementwise."
    )

    .def("__imul__", [](Matrix& mat, double scalar) -> Matrix&
        {
            mat = mat * scalar;
            return mat;
        },
        py::return_value_policy::reference_internal,
        py::arg("scalar"),
        "Multiply this matrix by a scalar."
    )

    .def("__itruediv__", [](Matrix& mat, const Matrix& other) -> Matrix&
        {
            mat = mat / other;
            return mat;
        },
        py::return_value_policy::reference_internal,
        py::arg("other"),
        "Divide this matrix by another matrix elementwise."
    )

    .def("__itruediv__", [](Matrix& mat, double scalar) -> Matrix&
        {
            mat = mat / scalar;
            return mat;
        },
        py::return_value_policy::reference_internal,
        py::arg("scalar"),
        "Divide this matrix by a scalar."
    )

    .def("__matmul__", &Matrix::matmul,
        py::arg("other"),
        "Return matrix multiplication when used as matrix @ matrix.")

    .def("__matmul__", [](const Matrix& mat, const Vector& vec)
        {
            return mat.matvec(vec);
        },
        py::arg("vector"),
        "Return matrix-vector multiplication when used as matrix @ vector."
    )

    .def("matmul", &Matrix::matmul,
        py::arg("other"),
        "Return matrix multiplication with another matrix.")

    .def("matvec", &Matrix::matvec,
        py::arg("vector"),
        "Return matrix-vector multiplication.")

    .def("vecmat", &Matrix::vecmat,
        py::arg("vector"),
        "Return vector-matrix multiplication using the supplied left-side vector.")

    .def("transpose", &Matrix::transpose,
        "Return the transposed matrix.")

    .def("determinant", &Matrix::determinant,
        "Return the determinant for a supported square matrix.")

    .def("inverse", &Matrix::inverse,
        "Return the inverse matrix. Currently not implemented.")

    .def("adjugate", &Matrix::adjugate,
        "Return the adjugate matrix. Currently not implemented.")

    .def("rref", &Matrix::rref,
        "Return the reduced row echelon form. Currently not implemented.")

    .def("rank", &Matrix::rank,
        "Return the matrix rank. Currently not implemented.")

    .def("__repr__", [](const Matrix& mat)
        {
            std::ostringstream oss;
            oss << mat;
            return oss.str();
        },
        "Return the string representation of the matrix."
    )

    .def("__contains__", [](const Matrix& mat, double value)
        {
            for (size_t row = 0; row < mat.getRows(); ++row) {
                for (size_t col = 0; col < mat.getCols(); ++col) {
                    if (mat(row, col) == value) {
                        return true;
                    }
                }
            }
            return false;
        },
        py::arg("value"),
        "Return True if the matrix contains value."
    );

}
