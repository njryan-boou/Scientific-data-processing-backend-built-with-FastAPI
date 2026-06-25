#include "../../include/Vector.hpp"

#include <cassert>
#include <cmath>
#include <iostream>

int main()
{
    Vector a({1.0, 2.0, 3.0});
    Vector b({4.0, 5.0, 6.0});

    assert(a.size() == 3);
    assert(a[0] == 1.0);
    a.set(0, 10.0);
    assert(a[0] == 10.0);
    a[0] = 1.0;

    Vector sum = a + b;
    Vector diff = b - a;
    Vector product = a * b;
    Vector quotient = b / a;

    assert(sum[2] == 9.0);
    assert(diff[0] == 3.0);
    assert(product[1] == 10.0);
    assert(quotient[2] == 2.0);
    assert((a * 2.0)[1] == 4.0);
    assert((b / 2.0)[2] == 3.0);

    assert(a.dot(b) == 32.0);
    assert(std::abs(a.magnitude() - std::sqrt(14.0)) < 1e-12);
    assert(a.cross(b)[0] == -3.0);

    std::cout << "test_vector_basics passed\n";
    return 0;
}
