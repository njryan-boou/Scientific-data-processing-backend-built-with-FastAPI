#include "../include/Vector.hpp"
#include "../include/Matrix.hpp"
#include <iostream>
#include <exception>

int main()
{
    Vector v1 = {1.0, 2.0, 3.0};
    Vector v2 = {4.0, 5.0, 6.06};
    
    Vector v3 = v1 + v2;
    std::cout << "v1 + v2 = " << v3 << std::endl;

    return 0;
}