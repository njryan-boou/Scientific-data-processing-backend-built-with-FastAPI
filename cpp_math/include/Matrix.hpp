#pragma once

#include <vector>
#include <initializer_list>

class Vector; // forward declaration if needed

class Matrix
{
private:
    size_t rows;
    size_t cols;
    std::vector<double> data;

public:
    Matrix(size_t rows, size_t cols);

    Matrix(
        size_t rows,
        size_t cols,
        std::initializer_list<double> values);

    Matrix(
        std::initializer_list<std::initializer_list<double>> values);

    size_t getRows() const;
    size_t getCols() const;

    // element access
    double& operator()(size_t row, size_t col);
    const double& operator()(size_t row, size_t col) const;

    // element-wise addition
    Matrix operator+(const Matrix& other) const;

    // element-wise subtraction
    Matrix operator-(const Matrix& other) const;

    // element-wise multiplication
    Matrix operator*(const Matrix& other) const;

    // element-wise division
    Matrix operator/(const Matrix& other) const;

    // matrix multiplication
    Matrix matmul(const Matrix& other) const;

    // print the matrix
    void print() const;
};