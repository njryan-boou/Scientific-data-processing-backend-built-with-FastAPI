#pragma once

#include <stdexcept>
#include <string>

namespace linalg
{

class LinalgError : public std::runtime_error
{
public:
    using std::runtime_error::runtime_error;
};

class ShapeError : public LinalgError
{
public:
    using LinalgError::LinalgError;
};

class DimensionError : public LinalgError
{
public:
    using LinalgError::LinalgError;
};

class IndexError : public LinalgError
{
public:
    using LinalgError::LinalgError;
};

class EmptyMatrixError : public LinalgError
{
public:
    using LinalgError::LinalgError;
};

class ValueError : public LinalgError
{
public:
    using LinalgError::LinalgError;
};

} // namespace linalg