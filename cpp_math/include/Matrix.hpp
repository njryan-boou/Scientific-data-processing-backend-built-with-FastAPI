#pragma once

#include "Vector.hpp"
#include "validation.hpp"

#include <cstddef>
#include <initializer_list>
#include <ostream>
#include <sstream>
#include <vector>

template <typename T = double>
class MatrixT
{
private:
    size_t row_count;
    size_t col_count;
    std::vector<T> data;

    static T mask_value(bool value)
    {
        return value ? T{1} : T{};
    }

    static bool is_truthy(T value)
    {
        return value != T{};
    }

public:
    using value_type = T;
    using iterator = typename std::vector<T>::iterator;
    using const_iterator = typename std::vector<T>::const_iterator;

    MatrixT(size_t rows, size_t cols)
        : row_count(rows),
          col_count(cols),
          data(rows * cols, T{})
    {
    }

    MatrixT(size_t rows, size_t cols, std::initializer_list<T> values)
        : row_count(rows),
          col_count(cols),
          data(values)
    {
        linalg::validate::reshape(values.size(), rows * cols);
    }

    MatrixT(std::initializer_list<std::initializer_list<T>> values)
    {
        row_count = values.size();
        col_count = values.size() == 0 ? 0 : values.begin()->size();

        data.reserve(row_count * col_count);
        for (const auto& row : values) {
            if (row.size() != col_count) {
                throw linalg::ShapeError("Jagged matrix");
            }
            data.insert(data.end(), row.begin(), row.end());
        }
    }

    MatrixT(const std::vector<std::vector<T>>& values)
    {
        row_count = values.size();
        col_count = values.empty() ? 0 : values[0].size();

        data.reserve(row_count * col_count);
        for (const auto& row : values) {
            if (row.size() != col_count) {
                throw linalg::ShapeError("Jagged matrix");
            }
            data.insert(data.end(), row.begin(), row.end());
        }
    }

    size_t getRows() const
    {
        return row_count;
    }

    size_t getCols() const
    {
        return col_count;
    }

    size_t rows() const
    {
        return row_count;
    }

    size_t cols() const
    {
        return col_count;
    }

    T& operator()(size_t row, size_t col)
    {
        linalg::validate::row(row, row_count);
        linalg::validate::column(col, col_count);
        return data.at(row * col_count + col);
    }

    const T& operator()(size_t row, size_t col) const
    {
        linalg::validate::row(row, row_count);
        linalg::validate::column(col, col_count);
        return data.at(row * col_count + col);
    }

    void set(size_t row, size_t col, T value)
    {
        linalg::validate::row(row, row_count);
        linalg::validate::column(col, col_count);
        data.at(row * col_count + col) = value;
    }

    iterator begin()
    {
        return data.begin();
    }

    iterator end()
    {
        return data.end();
    }

    const_iterator begin() const
    {
        return data.begin();
    }

    const_iterator end() const
    {
        return data.end();
    }

    const_iterator cbegin() const
    {
        return data.cbegin();
    }

    const_iterator cend() const
    {
        return data.cend();
    }

    MatrixT operator+(const MatrixT& other) const
    {
        linalg::validate::same_shape(*this, other);

        MatrixT result(row_count, col_count);
        for (size_t i = 0; i < data.size(); ++i) {
            result.data[i] = data[i] + other.data[i];
        }
        return result;
    }

    MatrixT operator-(const MatrixT& other) const
    {
        linalg::validate::same_shape(*this, other);

        MatrixT result(row_count, col_count);
        for (size_t i = 0; i < data.size(); ++i) {
            result.data[i] = data[i] - other.data[i];
        }
        return result;
    }

    MatrixT operator*(const MatrixT& other) const
    {
        linalg::validate::same_shape(*this, other);

        MatrixT result(row_count, col_count);
        for (size_t i = 0; i < data.size(); ++i) {
            result.data[i] = data[i] * other.data[i];
        }
        return result;
    }

    MatrixT operator/(const MatrixT& other) const
    {
        linalg::validate::same_shape(*this, other);

        MatrixT result(row_count, col_count);
        for (size_t i = 0; i < data.size(); ++i) {
            linalg::validate::require(other.data[i] != T{}, "Division by zero");
            result.data[i] = data[i] / other.data[i];
        }
        return result;
    }

    MatrixT operator*(T scalar) const
    {
        MatrixT result(row_count, col_count);
        for (size_t i = 0; i < data.size(); ++i) {
            result.data[i] = data[i] * scalar;
        }
        return result;
    }

    MatrixT operator/(T scalar) const
    {
        linalg::validate::require(scalar != T{}, "Division by zero");

        MatrixT result(row_count, col_count);
        for (size_t i = 0; i < data.size(); ++i) {
            result.data[i] = data[i] / scalar;
        }
        return result;
    }

    MatrixT operator==(const MatrixT& other) const
    {
        linalg::validate::same_shape(*this, other);

        MatrixT result(row_count, col_count);
        for (size_t i = 0; i < data.size(); ++i) {
            result.data[i] = mask_value(data[i] == other.data[i]);
        }
        return result;
    }

    MatrixT operator!=(const MatrixT& other) const
    {
        linalg::validate::same_shape(*this, other);

        MatrixT result(row_count, col_count);
        for (size_t i = 0; i < data.size(); ++i) {
            result.data[i] = mask_value(data[i] != other.data[i]);
        }
        return result;
    }

    MatrixT operator<(const MatrixT& other) const
    {
        linalg::validate::same_shape(*this, other);

        MatrixT result(row_count, col_count);
        for (size_t i = 0; i < data.size(); ++i) {
            result.data[i] = mask_value(data[i] < other.data[i]);
        }
        return result;
    }

    MatrixT operator<=(const MatrixT& other) const
    {
        linalg::validate::same_shape(*this, other);

        MatrixT result(row_count, col_count);
        for (size_t i = 0; i < data.size(); ++i) {
            result.data[i] = mask_value(data[i] <= other.data[i]);
        }
        return result;
    }

    MatrixT operator>(const MatrixT& other) const
    {
        linalg::validate::same_shape(*this, other);

        MatrixT result(row_count, col_count);
        for (size_t i = 0; i < data.size(); ++i) {
            result.data[i] = mask_value(data[i] > other.data[i]);
        }
        return result;
    }

    MatrixT operator>=(const MatrixT& other) const
    {
        linalg::validate::same_shape(*this, other);

        MatrixT result(row_count, col_count);
        for (size_t i = 0; i < data.size(); ++i) {
            result.data[i] = mask_value(data[i] >= other.data[i]);
        }
        return result;
    }

    MatrixT operator&(const MatrixT& other) const
    {
        linalg::validate::same_shape(*this, other);

        MatrixT result(row_count, col_count);
        for (size_t i = 0; i < data.size(); ++i) {
            result.data[i] = mask_value(is_truthy(data[i]) && is_truthy(other.data[i]));
        }
        return result;
    }

    MatrixT operator|(const MatrixT& other) const
    {
        linalg::validate::same_shape(*this, other);

        MatrixT result(row_count, col_count);
        for (size_t i = 0; i < data.size(); ++i) {
            result.data[i] = mask_value(is_truthy(data[i]) || is_truthy(other.data[i]));
        }
        return result;
    }

    MatrixT operator^(const MatrixT& other) const
    {
        linalg::validate::same_shape(*this, other);

        MatrixT result(row_count, col_count);
        for (size_t i = 0; i < data.size(); ++i) {
            result.data[i] = mask_value(is_truthy(data[i]) != is_truthy(other.data[i]));
        }
        return result;
    }

    MatrixT operator!() const
    {
        MatrixT result(row_count, col_count);
        for (size_t i = 0; i < data.size(); ++i) {
            result.data[i] = mask_value(!is_truthy(data[i]));
        }
        return result;
    }

    MatrixT matmul(const MatrixT& other) const
    {
        linalg::validate::multiplication(*this, other);

        MatrixT result(row_count, other.col_count);
        for (size_t i = 0; i < row_count; ++i) {
            for (size_t j = 0; j < other.col_count; ++j) {
                T sum{};
                for (size_t k = 0; k < col_count; ++k) {
                    sum += (*this)(i, k) * other(k, j);
                }
                result(i, j) = sum;
            }
        }
        return result;
    }

    VectorT<T> matvec(const VectorT<T>& vec) const
    {
        if (col_count != vec.size()) {
            std::ostringstream ss;
            ss << "Cannot multiply matrix of shape ("
               << row_count << ", " << col_count
               << ") by vector of size " << vec.size() << ".";
            throw linalg::DimensionError(ss.str());
        }

        VectorT<T> result(row_count);
        for (size_t i = 0; i < row_count; ++i) {
            T sum{};
            for (size_t j = 0; j < col_count; ++j) {
                sum += (*this)(i, j) * vec[j];
            }
            result[i] = sum;
        }
        return result;
    }

    VectorT<T> vecmat(const VectorT<T>& vec) const
    {
        if (row_count != vec.size()) {
            std::ostringstream ss;
            ss << "Cannot multiply vector of size "
               << vec.size()
               << " by matrix of shape ("
               << row_count << ", " << col_count << ").";
            throw linalg::DimensionError(ss.str());
        }

        VectorT<T> result(col_count);
        for (size_t j = 0; j < col_count; ++j) {
            T sum{};
            for (size_t i = 0; i < row_count; ++i) {
                sum += vec[i] * (*this)(i, j);
            }
            result[j] = sum;
        }
        return result;
    }

    MatrixT transpose() const
    {
        MatrixT result(col_count, row_count);
        for (size_t i = 0; i < row_count; ++i) {
            for (size_t j = 0; j < col_count; ++j) {
                result(j, i) = (*this)(i, j);
            }
        }
        return result;
    }

    T determinant2x2() const
    {
        if (row_count != 2 || col_count != 2) {
            std::ostringstream ss;
            ss << "Expected 2x2 matrix but got ("
               << row_count << ", " << col_count << ").";
            throw linalg::ShapeError(ss.str());
        }
        return (*this)(0, 0) * (*this)(1, 1) - (*this)(0, 1) * (*this)(1, 0);
    }

    T determinant3x3() const
    {
        if (row_count != 3 || col_count != 3) {
            std::ostringstream ss;
            ss << "Expected 3x3 matrix but got ("
               << row_count << ", " << col_count << ").";
            throw linalg::ShapeError(ss.str());
        }

        return (*this)(0, 0) * ((*this)(1, 1) * (*this)(2, 2) - (*this)(1, 2) * (*this)(2, 1)) -
               (*this)(0, 1) * ((*this)(1, 0) * (*this)(2, 2) - (*this)(1, 2) * (*this)(2, 0)) +
               (*this)(0, 2) * ((*this)(1, 0) * (*this)(2, 1) - (*this)(1, 1) * (*this)(2, 0));
    }

    T determinant() const
    {
        linalg::validate::not_empty(*this);
        linalg::validate::square(*this);

        if (row_count == 2) {
            return determinant2x2();
        }
        if (row_count == 3) {
            return determinant3x3();
        }
        throw linalg::ValueError("Determinant calculation is only implemented for 2x2 and 3x3 matrices");
    }

    MatrixT inverse() const
    {
        linalg::validate::not_empty(*this);
        linalg::validate::square(*this);
        throw linalg::ValueError("Inverse calculation not implemented");
    }

    MatrixT adjugate() const
    {
        linalg::validate::not_empty(*this);
        linalg::validate::square(*this);
        throw linalg::ValueError("Adjugate calculation not implemented");
    }

    MatrixT rref() const
    {
        linalg::validate::not_empty(*this);
        throw linalg::ValueError("RREF calculation not implemented");
    }

    size_t rank() const
    {
        linalg::validate::not_empty(*this);
        throw linalg::ValueError("Rank calculation not implemented");
    }

    friend std::ostream& operator<<(std::ostream& os, const MatrixT& mat)
    {
        for (size_t i = 0; i < mat.row_count; ++i) {
            os << "[ ";
            for (size_t j = 0; j < mat.col_count; ++j) {
                os << mat(i, j) << " ";
            }
            os << "]\n";
        }
        return os;
    }
};

using Matrix = MatrixT<double>;
