#include <iostream>
#include <stdexcept>
#include <vector>
#include <ostream>

#include "../include/Vector.hpp"
#include "../include/Matrix.hpp"


Matrix::Matrix(size_t rows, size_t cols)
    : rows(rows),
      cols(cols),
      data(rows * cols, 0.0)
{
}

Matrix::Matrix(
    size_t rows,
    size_t cols,
    std::initializer_list<double> values)
    : rows(rows),
      cols(cols),
      data(values)
{
    if (values.size() != rows * cols)
    {
        throw std::invalid_argument("Wrong number of values");
    }
}

Matrix::Matrix(
    std::initializer_list<std::initializer_list<double>> values)
{
    rows = values.size();
    cols = values.begin()->size();

    data.reserve(rows * cols);

    for (const auto& row : values)
    {
        if (row.size() != cols)
        {
            throw std::invalid_argument("Jagged matrix");
        }

        data.insert(data.end(), row.begin(), row.end());
    }
}


Matrix::Matrix(const std::vector<std::vector<double>>& values)
{
    rows = values.size();
    cols = values.empty() ? 0 : values[0].size();

    data.reserve(rows * cols);

    for (const auto& row : values)
    {
        if (row.size() != cols)
        {
            throw std::invalid_argument("Jagged matrix");
        }

        data.insert(data.end(), row.begin(), row.end());
    }
}

size_t Matrix::getRows() const
{
    return rows;
}

size_t Matrix::getCols() const
{
    return cols;
}

double& Matrix::operator()(size_t row, size_t col) 
{
    return data.at(row * cols + col);
}

const double& Matrix::operator()(size_t row, size_t col) const
{
    return data.at(row * cols + col);
}

void Matrix::set(size_t row, size_t col, double value)
{
    data.at(row * cols + col) = value;
}

Matrix Matrix::operator+(const Matrix& other) const
{
    if (rows != other.rows || cols != other.cols)
    {
        throw std::invalid_argument("Matrix shapes must match");
    }

    Matrix result(rows, cols);

    for (size_t i = 0; i < data.size(); ++i)
    {
        result.data[i] = data[i] + other.data[i];
    }

    return result;
}

Matrix Matrix::operator-(const Matrix& other) const
{
    if (rows != other.rows || cols != other.cols)
    {
        throw std::invalid_argument("Matrix shapes must match");
    }

    Matrix result(rows, cols);

    for (size_t i = 0; i < data.size(); ++i)
    {
        result.data[i] = data[i] - other.data[i];
    }

    return result;
}

Matrix Matrix::operator*(const Matrix& other) const
{
    if (rows != other.rows || cols != other.cols)
    {
        throw std::invalid_argument("Matrix shapes must match");
    }

    Matrix result(rows, cols);

    for (size_t i = 0; i < data.size(); ++i)
    {
        result.data[i] = data[i] * other.data[i];
    }

    return result;
}

Matrix Matrix::operator/(const Matrix& other) const
{
    if (rows != other.rows || cols != other.cols)
    {
        throw std::invalid_argument("Matrix shapes must match");
    }

    Matrix result(rows, cols);

    for (size_t i = 0; i < data.size(); ++i)
    {
        if (other.data[i] == 0.0)
        {
            throw std::invalid_argument("Division by zero");
        }
        result.data[i] = data[i] / other.data[i];
    }

    return result;
}


Matrix Matrix::operator*(double scalar) const
{
    Matrix result(rows, cols);

    for (size_t i = 0; i < data.size(); ++i)
    {
        result.data[i] = data[i] * scalar;
    }

    return result;
}


Matrix Matrix::operator/(double scalar) const
{
    if (scalar == 0.0)
    {
        throw std::invalid_argument("Division by zero");
    }

    Matrix result(rows, cols);

    for (size_t i = 0; i < data.size(); ++i)
    {
        result.data[i] = data[i] / scalar;
    }

    return result;
}

Matrix Matrix::matmul(const Matrix& other) const
{
    if (cols != other.rows)
    {
        throw std::invalid_argument("Matrix shapes not compatible for multiplication");
    }

    Matrix result(rows, other.cols);

    for (size_t i = 0; i < rows; ++i)
    {
        for (size_t j = 0; j < other.cols; ++j)
        {
            double sum = 0.0;
            for (size_t k = 0; k < cols; ++k)
            {
                sum += (*this)(i, k) * other(k, j);
            }
            result(i, j) = sum;
        }
    }

    return result;
}

Vector Matrix::matvec(const Vector& vec) const
{
    if (cols != vec.size())
    {
        throw std::invalid_argument("Matrix and vector shapes not compatible for multiplication");
    }

    Vector result(rows);

    for (size_t i = 0; i < rows; ++i)
    {
        double sum = 0.0;
        for (size_t j = 0; j < cols; ++j)
        {
            sum += (*this)(i, j) * vec[j];
        }
        result[i] = sum;
    }

    return result;
}


Vector Matrix::vecmat(const Vector& vec) const
{
    if (rows != vec.size())
    {
        throw std::invalid_argument("Matrix and vector shapes not compatible for multiplication");
    }

    Vector result(cols);

    for (size_t j = 0; j < cols; ++j)
    {
        double sum = 0.0;
        for (size_t i = 0; i < rows; ++i)
        {
            sum += vec[i] * (*this)(i, j);
        }
        result[j] = sum;
    }

    return result;
}


Matrix Matrix::transpose() const
{
    Matrix result(cols, rows);

    for (size_t i = 0; i < rows; ++i)
    {
        for (size_t j = 0; j < cols; ++j)
        {
            result(j, i) = (*this)(i, j);
        }
    }

    return result;
}


double Matrix::determinant2x2() const
{
    if (rows != 2 || cols != 2)
    {
        throw std::invalid_argument("Determinant is only defined for 2x2 matrices");
    }

    return (*this)(0, 0) * (*this)(1, 1) - (*this)(0, 1) * (*this)(1, 0);
}


double Matrix::determinant3x3() const
{
    if (rows != 3 || cols != 3)
    {
        throw std::invalid_argument("Determinant is only defined for 3x3 matrices");
    }

    return (*this)(0, 0) * ((*this)(1, 1) * (*this)(2, 2) - (*this)(1, 2) * (*this)(2, 1)) -
           (*this)(0, 1) * ((*this)(1, 0) * (*this)(2, 2) - (*this)(1, 2) * (*this)(2, 0)) +
           (*this)(0, 2) * ((*this)(1, 0) * (*this)(2, 1) - (*this)(1, 1) * (*this)(2, 0));
}


double Matrix::determinant() const
{
    if (rows != cols)
    {
        throw std::invalid_argument("Determinant is only defined for square matrices");
    }

    if (rows == 2)
    {
        return determinant2x2();
    }
    else if (rows == 3)
    {
        return determinant3x3();
    }
    else
    {
        throw std::invalid_argument("Determinant calculation is only implemented for 2x2 and 3x3 matrices");
    }
}


Matrix Matrix::inverse() const
{
    // This is a placeholder implementation. A proper inverse calculation would require
    // implementing Gaussian elimination or similar methods.
    throw std::logic_error("Inverse calculation not implemented");
}


Matrix Matrix::rref() const
{
    // This is a placeholder implementation. A proper RREF calculation would require
    // implementing Gaussian elimination or similar methods.
    throw std::logic_error("RREF calculation not implemented");
}


size_t Matrix::rank() const
{
    // This is a placeholder implementation. A proper rank calculation would require
    // implementing Gaussian elimination or similar methods.
    throw std::logic_error("Rank calculation not implemented");
}


Matrix Matrix::adjugate() const
{
    // This is a placeholder implementation. A proper adjugate calculation would require
    // implementing cofactor expansion or similar methods.
    throw std::logic_error("Adjugate calculation not implemented");
}


std::ostream& operator<<(std::ostream& os, const Matrix& mat)
{
    for (size_t i = 0; i < mat.rows; ++i)
    {
        os << "[ ";

        for (size_t j = 0; j < mat.cols; ++j)
        {
            os << mat(i, j) << ", ";
        }

        os << "]\n";
    }
    return os;
}