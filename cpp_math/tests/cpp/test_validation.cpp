#include "../../include/Matrix.hpp"
#include "../../include/Vector.hpp"
#include "../../include/exceptions.hpp"
#include "../../include/validation.hpp"

#include <cassert>
#include <iostream>

int main()
{
    Matrix square({{1.0, 2.0}, {3.0, 4.0}});
    Matrix wide({{1.0, 2.0, 3.0}});

    linalg::validate::square(square);
    linalg::validate::same_shape(square, square);
    linalg::validate::multiplication(square, square);
    linalg::validate::row(1, square.rows());
    linalg::validate::column(1, square.cols());
    linalg::validate::positive_dimension(square.rows(), "rows");
    linalg::validate::reshape(4, square.rows() * square.cols());

    bool caught_shape = false;
    try {
        wide.determinant();
    } catch (const linalg::ShapeError&) {
        caught_shape = true;
    }
    assert(caught_shape);

    bool caught_dimension = false;
    try {
        wide.matmul(wide);
    } catch (const linalg::DimensionError&) {
        caught_dimension = true;
    }
    assert(caught_dimension);

    bool caught_index = false;
    try {
        square(2, 0);
    } catch (const linalg::IndexError&) {
        caught_index = true;
    }
    assert(caught_index);

    bool caught_value = false;
    try {
        Vector({1.0}) + Vector({1.0, 2.0});
    } catch (const linalg::ValueError&) {
        caught_value = true;
    }
    assert(caught_value);

    std::cout << "test_validation passed\n";
    return 0;
}
