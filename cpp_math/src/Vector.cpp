#include "../include/Vector.hpp"
#include "../include/Matrix.hpp"

#include <iostream>
#include <ostream>
#include <stdexcept>
#include <cmath>


Vector::Vector(size_t size)
    : data(size, 0.0)
{
}


Vector::Vector(const std::vector<double>& values)
    : data(values)
{
}


Vector::Vector(std::initializer_list<double> values)
    : data(values)
{
}


size_t Vector::size() const
{
    return data.size();
}


double& Vector::operator[](size_t index)
{
    return data.at(index);
}


const double& Vector::operator[](size_t index) const
{
    return data.at(index);
}


void Vector::set(size_t index, double value)
{
    data.at(index) = value;
}


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


Vector Vector::operator-(const Vector& other) const
{
    if (size() != other.size()) {
        throw std::invalid_argument("Vector sizes must match");
    }

    Vector result(size());

    for (size_t i = 0; i < size(); i++) {
        result[i] = data[i] - other[i];
    }

    return result;
}


Vector Vector::operator*(const Vector& other) const
{
    if (size() != other.size()) {
        throw std::invalid_argument("Vector sizes must match");
    }

    Vector result(size());

    for (size_t i = 0; i < size(); i++) {
        result[i] = data[i] * other[i];
    }

    return result;
}


Vector Vector::operator/(const Vector& other) const
{
    if (size() != other.size()) {
        throw std::invalid_argument("Vector sizes must match");
    }

    Vector result(size());

    for (size_t i = 0; i < size(); i++) {
        if (other[i] == 0.0) {
            throw std::invalid_argument("Division by zero");
        }
        result[i] = data[i] / other[i];
    }

    return result;
}


Vector Vector::operator*(double scalar) const
{
    Vector result(size());

    for (size_t i = 0; i < size(); i++) {
        result[i] = data[i] * scalar;
    }

    return result;
}


Vector Vector::operator/(double scalar) const
{
    if (scalar == 0.0) {
        throw std::invalid_argument("Division by zero");
    }

    Vector result(size());

    for (size_t i = 0; i < size(); i++) {
        result[i] = data[i] / scalar;
    }

    return result;
}


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


double Vector::magnitude() const
{

    return std::sqrt(dot(*this));
}


Vector Vector::normalize() const
{
    double mag = magnitude();

    if (mag == 0.0) {
        throw std::invalid_argument("Cannot normalize a zero vector");
    }

    Vector result(size());

    for (size_t i = 0; i < size(); i++) {
        result[i] = data[i] / mag;
    }

    return result;
}


Vector Vector::cross(const Vector& other) const
{
    if (size() != 3 || other.size() != 3) {
        throw std::invalid_argument("Cross product is only defined for 3D vectors");
    }

    Vector result(3);

    result[0] = data[1] * other[2] - data[2] * other[1];
    result[1] = data[2] * other[0] - data[0] * other[2];
    result[2] = data[0] * other[1] - data[1] * other[0];

    return result;
}


Vector Vector::solve(const Matrix& A) const
{
    // This is a placeholder implementation. A proper linear system solver would require
    // implementing Gaussian elimination or similar methods.
    throw std::logic_error("Linear system solver not implemented");
}


std::ostream& operator<<(std::ostream& os, const Vector& vec)
{
    os << "[ ";

    for (double value : vec.data) {
        os << value << ", ";
    }

    os << "]";
    return os;
}