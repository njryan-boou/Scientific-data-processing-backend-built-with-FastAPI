#include "../../include/Matrix.hpp"
#include "../../include/Vector.hpp"

#include <cassert>
#include <iostream>

int main()
{
    VectorT<float> floats({1.0f, 2.0f, 3.0f});
    VectorT<float> more_floats({4.0f, 5.0f, 6.0f});
    VectorT<float> float_sum = floats + more_floats;

    assert(float_sum.size() == 3);
    assert(float_sum[0] == 5.0f);
    assert(floats.dot(more_floats) == 32.0f);

    MatrixT<int> ints({{1, 2}, {3, 4}});
    MatrixT<int> more_ints({{5, 6}, {7, 8}});
    MatrixT<int> int_product = ints.matmul(more_ints);

    assert(int_product(0, 0) == 19);
    assert(int_product(1, 1) == 50);
    assert(ints.determinant() == -2);

    std::cout << "test_templates passed\n";
    return 0;
}
