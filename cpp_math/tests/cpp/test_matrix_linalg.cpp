#include "../../include/Matrix.hpp"

#include <cassert>
#include <iostream>

int main()
{
    Matrix a({{1.0, 2.0}, {3.0, 4.0}});
    Matrix b({{5.0, 6.0}, {7.0, 8.0}});
    Vector v({2.0, 3.0});

    Matrix product = a.matmul(b);
    assert(product(0, 0) == 19.0);
    assert(product(0, 1) == 22.0);
    assert(product(1, 0) == 43.0);
    assert(product(1, 1) == 50.0);

    Vector matvec = a.matvec(v);
    assert(matvec[0] == 8.0);
    assert(matvec[1] == 18.0);

    Vector vecmat = a.vecmat(v);
    assert(vecmat[0] == 11.0);
    assert(vecmat[1] == 16.0);

    assert(a.determinant() == -2.0);

    Matrix c({{6.0, 1.0, 1.0}, {4.0, -2.0, 5.0}, {2.0, 8.0, 7.0}});
    assert(c.determinant() == -306.0);

    std::cout << "test_matrix_linalg passed\n";
    return 0;
}
