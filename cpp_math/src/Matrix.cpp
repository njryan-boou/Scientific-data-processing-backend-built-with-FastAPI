#include <iostream>
#include <stdexcept>
#include <vector>

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

void Matrix::print() const
{
    for (size_t i = 0; i < rows; ++i)
    {
        std::cout << "[ ";

        for (size_t j = 0; j < cols; ++j)
        {
            std::cout << (*this)(i, j) << ' ';
        }

        std::cout << "]\n";
    }
}