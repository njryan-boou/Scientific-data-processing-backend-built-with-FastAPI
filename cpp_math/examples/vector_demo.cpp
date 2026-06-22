// vector_demo.cpp
#include <iostream>
#include "Vector.hpp"
#include "Matrix.hpp"

int main() {
    Matrix mat1 = {
        {1.0, 2.0, 3.0},
        {4.0, 5.0, 6.0}
    };

    Matrix mat2 = {
        {7.0, 8.0, 9.0},
        {10.0, 11.0, 12.0}
    };

    Matrix result = mat1.matmul(mat2);
    result.print();

    return 0;
}