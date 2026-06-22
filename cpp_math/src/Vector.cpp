#include "../include/Vector.hpp"

#include <iostream>
#include <stdexcept>

// Constructors

Vector::Vector(size_t size)
    : data(size, 0.0)
{
}

Vector::Vector(std::initializer_list<double> values)
    : data(values)
{
}

// Size

size_t Vector::size() const
{
    return data.size();
}

// Element access

double& Vector::operator[](size_t index)
{
    return data.at(index);
}

const double& Vector::operator[](size_t index) const
{
    return data.at(index);
}

// Addition

Vector Vector::operator+(const Vector& other) const
{
    if (size() != other.size()) {
        throw std::invalid_argument("Vector sizes must match");
    }

    Vector result(size());

    for (size_t i = 0; i < size(); i++) {
        result[i] = data[i] + other[i];
    }

    return result;
}

// Dot product

double Vector::dot(const Vector& other) const
{
    if (size() != other.size()) {
        throw std::invalid_argument("Vector sizes must match");
    }

    double sum = 0.0;

    for (size_t i = 0; i < size(); i++) {
        sum += data[i] * other[i];
    }

    return sum;
}

// Print

void Vector::print() const
{
    std::cout << "[ ";

    for (double value : data) {
        std::cout << value << " ";
    }

    std::cout << "]\n";
}