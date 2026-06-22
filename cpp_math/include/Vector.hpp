#pragma once

#include <vector>
#include <initializer_list>

class Vector {
private:
    std::vector<double> data;

public:
    Vector(size_t size);
    Vector(std::initializer_list<double> values);

    size_t size() const;

    double& operator[](size_t index);
    const double& operator[](size_t index) const;

    Vector operator+(const Vector& other) const;

    double dot(const Vector& other) const;

    void print() const;
};