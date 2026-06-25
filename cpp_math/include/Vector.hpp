#pragma once

#include "validation.hpp"

#include <cmath>
#include <cstddef>
#include <initializer_list>
#include <ostream>
#include <vector>

template <typename T>
class MatrixT;

template <typename T = double>
class VectorT {
private:
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

    VectorT(size_t size)
        : data(size, T{})
    {
    }

    VectorT(std::initializer_list<T> values)
        : data(values)
    {
    }

    VectorT(const std::vector<T>& values)
        : data(values)
    {
    }

    size_t size() const
    {
        return data.size();
    }

    T& operator[](size_t index)
    {
        return data.at(index);
    }

    const T& operator[](size_t index) const
    {
        return data.at(index);
    }

    void set(size_t index, T value)
    {
        data.at(index) = value;
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

    VectorT operator+(const VectorT& other) const
    {
        linalg::validate::require(size() == other.size(), "Vector sizes must match");

        VectorT result(size());
        for (size_t i = 0; i < size(); i++) {
            result[i] = data[i] + other[i];
        }
        return result;
    }

    VectorT operator-(const VectorT& other) const
    {
        linalg::validate::require(size() == other.size(), "Vector sizes must match");

        VectorT result(size());
        for (size_t i = 0; i < size(); i++) {
            result[i] = data[i] - other[i];
        }
        return result;
    }

    VectorT operator*(const VectorT& other) const
    {
        linalg::validate::require(size() == other.size(), "Vector sizes must match");

        VectorT result(size());
        for (size_t i = 0; i < size(); i++) {
            result[i] = data[i] * other[i];
        }
        return result;
    }

    VectorT operator/(const VectorT& other) const
    {
        linalg::validate::require(size() == other.size(), "Vector sizes must match");

        VectorT result(size());
        for (size_t i = 0; i < size(); i++) {
            linalg::validate::require(other[i] != T{}, "Division by zero");
            result[i] = data[i] / other[i];
        }
        return result;
    }

    VectorT operator*(T scalar) const
    {
        VectorT result(size());
        for (size_t i = 0; i < size(); i++) {
            result[i] = data[i] * scalar;
        }
        return result;
    }

    VectorT operator/(T scalar) const
    {
        linalg::validate::require(scalar != T{}, "Division by zero");

        VectorT result(size());
        for (size_t i = 0; i < size(); i++) {
            result[i] = data[i] / scalar;
        }
        return result;
    }

    VectorT operator==(const VectorT& other) const
    {
        linalg::validate::require(size() == other.size(), "Vector sizes must match");

        VectorT result(size());
        for (size_t i = 0; i < size(); i++) {
            result[i] = mask_value(data[i] == other[i]);
        }
        return result;
    }

    VectorT operator!=(const VectorT& other) const
    {
        linalg::validate::require(size() == other.size(), "Vector sizes must match");

        VectorT result(size());
        for (size_t i = 0; i < size(); i++) {
            result[i] = mask_value(data[i] != other[i]);
        }
        return result;
    }

    VectorT operator<(const VectorT& other) const
    {
        linalg::validate::require(size() == other.size(), "Vector sizes must match");

        VectorT result(size());
        for (size_t i = 0; i < size(); i++) {
            result[i] = mask_value(data[i] < other[i]);
        }
        return result;
    }

    VectorT operator<=(const VectorT& other) const
    {
        linalg::validate::require(size() == other.size(), "Vector sizes must match");

        VectorT result(size());
        for (size_t i = 0; i < size(); i++) {
            result[i] = mask_value(data[i] <= other[i]);
        }
        return result;
    }

    VectorT operator>(const VectorT& other) const
    {
        linalg::validate::require(size() == other.size(), "Vector sizes must match");

        VectorT result(size());
        for (size_t i = 0; i < size(); i++) {
            result[i] = mask_value(data[i] > other[i]);
        }
        return result;
    }

    VectorT operator>=(const VectorT& other) const
    {
        linalg::validate::require(size() == other.size(), "Vector sizes must match");

        VectorT result(size());
        for (size_t i = 0; i < size(); i++) {
            result[i] = mask_value(data[i] >= other[i]);
        }
        return result;
    }

    VectorT operator&(const VectorT& other) const
    {
        linalg::validate::require(size() == other.size(), "Vector sizes must match");

        VectorT result(size());
        for (size_t i = 0; i < size(); i++) {
            result[i] = mask_value(is_truthy(data[i]) && is_truthy(other[i]));
        }
        return result;
    }

    VectorT operator|(const VectorT& other) const
    {
        linalg::validate::require(size() == other.size(), "Vector sizes must match");

        VectorT result(size());
        for (size_t i = 0; i < size(); i++) {
            result[i] = mask_value(is_truthy(data[i]) || is_truthy(other[i]));
        }
        return result;
    }

    VectorT operator^(const VectorT& other) const
    {
        linalg::validate::require(size() == other.size(), "Vector sizes must match");

        VectorT result(size());
        for (size_t i = 0; i < size(); i++) {
            result[i] = mask_value(is_truthy(data[i]) != is_truthy(other[i]));
        }
        return result;
    }

    VectorT operator!() const
    {
        VectorT result(size());
        for (size_t i = 0; i < size(); i++) {
            result[i] = mask_value(!is_truthy(data[i]));
        }
        return result;
    }

    T dot(const VectorT& other) const
    {
        linalg::validate::require(size() == other.size(), "Vector sizes must match");

        T sum{};
        for (size_t i = 0; i < size(); i++) {
            sum += data[i] * other[i];
        }
        return sum;
    }

    double magnitude() const
    {
        return std::sqrt(static_cast<double>(dot(*this)));
    }

    VectorT normalize() const
    {
        double mag = magnitude();
        linalg::validate::require(mag != 0.0, "Cannot normalize a zero vector");

        VectorT result(size());
        for (size_t i = 0; i < size(); i++) {
            result[i] = static_cast<T>(data[i] / mag);
        }
        return result;
    }

    VectorT cross(const VectorT& other) const
    {
        linalg::validate::require(
            size() == 3 && other.size() == 3,
            "Cross product is only defined for 3D vectors");

        VectorT result(3);
        result[0] = data[1] * other[2] - data[2] * other[1];
        result[1] = data[2] * other[0] - data[0] * other[2];
        result[2] = data[0] * other[1] - data[1] * other[0];
        return result;
    }

    VectorT solve(const MatrixT<T>&) const
    {
        throw linalg::ValueError("Linear system solver not implemented");
    }

    friend std::ostream& operator<<(std::ostream& os, const VectorT& vec)
    {
        os << "[ ";
        for (const T& value : vec.data) {
            os << value << " ";
        }
        os << "]";
        return os;
    }
};

using Vector = VectorT<double>;
