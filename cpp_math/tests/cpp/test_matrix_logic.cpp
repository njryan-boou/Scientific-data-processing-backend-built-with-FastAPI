#include "../../include/Matrix.hpp"

#include <cassert>
#include <iostream>

int main()
{
    Matrix a({{0.0, 2.0}, {3.0, 4.0}});
    Matrix b({{1.0, 2.0}, {2.0, 5.0}});

    assert((a == b)(0, 0) == 0.0);
    assert((a == b)(0, 1) == 1.0);
    assert((a != b)(1, 1) == 1.0);
    assert((a < b)(0, 0) == 1.0);
    assert((a <= b)(0, 1) == 1.0);
    assert((a > b)(1, 0) == 1.0);
    assert((a >= b)(0, 1) == 1.0);

    assert((a & b)(0, 0) == 0.0);
    assert((a & b)(1, 0) == 1.0);
    assert((a | b)(0, 0) == 1.0);
    assert((a ^ b)(0, 0) == 1.0);
    assert((!a)(0, 0) == 1.0);
    assert((!a)(1, 0) == 0.0);

    std::cout << "test_matrix_logic passed\n";
    return 0;
}
