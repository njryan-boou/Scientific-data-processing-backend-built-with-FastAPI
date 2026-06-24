#pragma once

#include <vector>
#include <initializer_list>
#include <ostream>

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

    // Constructor from std::vector
    Matrix(const std::vector<std::vector<double>>& values);

    size_t getRows() const;
    size_t getCols() const;

    // element access
    double& operator()(size_t row, size_t col);
    const double& operator()(size_t row, size_t col) const;

    // set item
    void set(size_t row, size_t col, double value);

    // element-wise addition
    Matrix operator+(const Matrix& other) const;

    // element-wise subtraction
    Matrix operator-(const Matrix& other) const;

    // element-wise multiplication
    Matrix operator*(const Matrix& other) const;

    // element-wise division
    Matrix operator/(const Matrix& other) const;

    // scalar multiplication
    Matrix operator*(double scalar) const;

    // scalar division
    Matrix operator/(double scalar) const;

    // matrix multiplication
    Matrix matmul(const Matrix& other) const;

    // matrix-vector multiplication
    Vector matvec(const Vector& vec) const;

    // vector-matrix multiplication
    Vector vecmat(const Vector& vec) const;

    // transpose of the matrix
    Matrix transpose() const;

    // determinant 2x2
    double determinant2x2() const;

    // determinant 3x3
    double determinant3x3() const;

    // determinant
    double determinant() const;

    // inverse of the matrix
    Matrix inverse() const;

    // adjugate of the matrix
    Matrix adjugate() const;

    // RREF (Reduced Row Echelon Form)
    Matrix rref() const;

    // rank of the matrix
    size_t rank() const;

    // << operator for printing
    friend std::ostream& operator<<(std::ostream& os, const Matrix& mat);
};