#include <pybind11/pybind11.h>
#include "../include/Vector.hpp"

namespace py = pybind11;

PYBIND11_MODULE(matrix_engine, m)
{
	m.doc() = "Matrix/vector engine bindings";
	m.def("add", &add, "Add two numbers");
}
