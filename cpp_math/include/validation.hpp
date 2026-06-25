#pragma once

#include <sstream>
#include <string>

#include "exceptions.hpp"

namespace linalg::validate
{

//--------------------------------------------------
// Generic
//--------------------------------------------------

inline void require(bool condition, const std::string& message)
{
    if (!condition)
        throw ValueError(message);
}

//--------------------------------------------------
// Bounds
//--------------------------------------------------

inline void row(std::size_t index, std::size_t rows)
{
    if (index >= rows)
    {
        std::ostringstream ss;
        ss << "Row index "
           << index
           << " is out of bounds for matrix with "
           << rows
           << " rows.";

        throw IndexError(ss.str());
    }
}

inline void column(std::size_t index, std::size_t cols)
{
    if (index >= cols)
    {
        std::ostringstream ss;
        ss << "Column index "
           << index
           << " is out of bounds for matrix with "
           << cols
           << " columns.";

        throw IndexError(ss.str());
    }
}

//--------------------------------------------------
// Matrix properties
//--------------------------------------------------

template<typename Matrix>
inline void not_empty(const Matrix& m)
{
    if (m.rows() == 0 || m.cols() == 0)
        throw EmptyMatrixError(
            "Matrix cannot be empty."
        );
}

template<typename Matrix>
inline void square(const Matrix& m)
{
    if (m.rows() != m.cols())
    {
        std::ostringstream ss;

        ss << "Expected square matrix but got ("
           << m.rows()
           << ", "
           << m.cols()
           << ").";

        throw ShapeError(ss.str());
    }
}

//--------------------------------------------------
// Binary operations
//--------------------------------------------------

template<typename A, typename B>
inline void same_shape(
    const A& lhs,
    const B& rhs)
{
    if (lhs.rows() != rhs.rows() ||
        lhs.cols() != rhs.cols())
    {
        std::ostringstream ss;

        ss << "Shape mismatch: ("
           << lhs.rows()
           << ", "
           << lhs.cols()
           << ") vs ("
           << rhs.rows()
           << ", "
           << rhs.cols()
           << ").";

        throw ShapeError(ss.str());
    }
}

template<typename A, typename B>
inline void multiplication(
    const A& lhs,
    const B& rhs)
{
    if (lhs.cols() != rhs.rows())
    {
        std::ostringstream ss;

        ss << "Cannot multiply matrices of shape ("
           << lhs.rows()
           << ", "
           << lhs.cols()
           << ") and ("
           << rhs.rows()
           << ", "
           << rhs.cols()
           << ").";

        throw DimensionError(ss.str());
    }
}

//--------------------------------------------------
// Shape utilities
//--------------------------------------------------

inline void positive_dimension(
    std::size_t value,
    const std::string& name)
{
    if (value == 0)
    {
        std::ostringstream ss;

        ss << name
           << " must be greater than zero.";

        throw DimensionError(ss.str());
    }
}

inline void reshape(
    std::size_t current,
    std::size_t requested)
{
    if (current != requested)
    {
        std::ostringstream ss;

        ss << "Cannot reshape "
           << current
           << " elements into "
           << requested
           << " elements.";

        throw ShapeError(ss.str());
    }
}

} // namespace linalg::validate