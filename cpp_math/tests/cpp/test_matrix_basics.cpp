#include "../../include/Matrix.hpp"

#include <cassert>
#include <iostream>

int main()
{
    Matrix a({{1.0, 2.0}, {3.0, 4.0}});
    Matrix b({{5.0, 6.0}, {7.0, 8.0}});

    assert(a.rows() == 2);
    assert(a.cols() == 2);
    assert(a.getRows() == 2);
    assert(a.getCols() == 2);
    assert(a(1, 0) == 3.0);

    a.set(1, 0, 9.0);
    assert(a(1, 0) == 9.0);
    a(1, 0) = 3.0;

    Matrix sum = a + b;
    Matrix diff = b - a;
    Matrix product = a * b;
    Matrix quotient = b / a;

    assert(sum(1, 1) == 12.0);
    assert(diff(0, 0) == 4.0);
    assert(product(1, 1) == 32.0);
    assert(quotient(1, 1) == 2.0);
    assert((a * 2.0)(0, 1) == 4.0);
    assert((b / 2.0)(1, 1) == 4.0);

    Matrix transposed = a.transpose();
    assert(transposed(0, 1) == 3.0);
    assert(transposed(1, 0) == 2.0);

    std::cout << "test_matrix_basics passed\n";
    return 0;
}
