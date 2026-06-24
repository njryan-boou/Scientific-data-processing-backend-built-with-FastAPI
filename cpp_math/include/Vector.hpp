#pragma once
#include <ostream>
#include <cstddef>

#include <vector>
#include <initializer_list>

class Vector {
private:
    std::vector<double> data;

public:
    // Constructors
    Vector(size_t size);

    // Constructor from initializer list
    Vector(std::initializer_list<double> values);

    // std vector constructor
    Vector(const std::vector<double>& values);

    // Get the size of the vector
    size_t size() const;

    // Element access
    double& operator[](size_t index);

    // Element access (const version)
    const double& operator[](size_t index) const;

    // Set item
    void set(size_t index, double value);


    // Addition
    Vector operator+(const Vector& other) const;

    // Subtraction
    Vector operator-(const Vector& other) const;

    // Element-wise multiplication
    Vector operator*(const Vector& other) const;

    // Element-wise division
    Vector operator/(const Vector& other) const;

    // scalar multiplication
    Vector operator*(double scalar) const;

    // scalar division
    Vector operator/(double scalar) const;

    // Dot product
    double dot(const Vector& other) const;

    // Magnitude of the vector
    double magnitude() const;

    // Normalize the vector
    Vector normalize() const;

    // Cross product (only for 3D vectors)
    Vector cross(const Vector& other) const;

    // solve linear system Ax = b, where A is a matrix and b is this vector
    Vector solve(const class Matrix& A) const;

    // << operator for printing
    friend std::ostream& operator<<(std::ostream& os, const Vector& vec);
};