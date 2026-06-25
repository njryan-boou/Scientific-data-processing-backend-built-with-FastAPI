#include "../../include/Vector.hpp"

#include <cassert>
#include <iostream>

int main()
{
    Vector a({0.0, 2.0, 3.0});
    Vector b({1.0, 2.0, 4.0});

    assert((a == b)[0] == 0.0);
    assert((a == b)[1] == 1.0);
    assert((a != b)[2] == 1.0);
    assert((a < b)[0] == 1.0);
    assert((a <= b)[1] == 1.0);
    assert((b > a)[2] == 1.0);
    assert((b >= a)[1] == 1.0);

    assert((a & b)[0] == 0.0);
    assert((a | b)[0] == 1.0);
    assert((a ^ b)[0] == 1.0);
    assert((!a)[0] == 1.0);
    assert((!a)[1] == 0.0);

    std::cout << "test_vector_logic passed\n";
    return 0;
}
