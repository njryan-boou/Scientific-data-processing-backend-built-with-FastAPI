# Matrix Engine

Header-only C++ vector and matrix templates with Python bindings built through
pybind11.

## Features

- Header-only C++ templates: `VectorT<T>` and `MatrixT<T>`
- Python API using double-based aliases: `Vector` and `Matrix`
- Vector arithmetic, dot product, magnitude, normalization, and 3D cross product
- Matrix arithmetic, transpose, matrix multiplication, matrix-vector multiplication, and determinant for 2x2 and 3x3 matrices
- Elementwise comparison and logical mask operators
- Row iteration for matrices in Python
- Custom validation helpers and exception types exposed to Python
- C++ tests through CTest and Python tests through `unittest`

## Layout

```text
cpp_math/
  include/              C++ headers
  matrix_engine/        Python package files and built extension output
  python/               pybind11 bindings
  tests/cpp/            C++ tests
  tests/python/         Python tests
  examples/             C++ examples
```

## C++ Usage

```cpp
#include "Matrix.hpp"
#include "Vector.hpp"

#include <iostream>

int main()
{
    Vector v({1.0, 2.0, 3.0});
    Vector w({4.0, 5.0, 6.0});

    std::cout << v.dot(w) << "\n";

    Matrix A({{1.0, 2.0}, {3.0, 4.0}});
    Matrix B({{5.0, 6.0}, {7.0, 8.0}});

    std::cout << A.matmul(B);
}
```

The default aliases use `double`:

```cpp
using Vector = VectorT<double>;
using Matrix = MatrixT<double>;
```

You can also use other numeric types:

```cpp
VectorT<float> vf({1.0f, 2.0f});
MatrixT<int> mi({{1, 2}, {3, 4}});
```

## Python Usage

```python
import matrix_engine as me

v = me.Vector([1.0, 2.0, 3.0])
w = me.Vector([4.0, 5.0, 6.0])

print(v @ w)          # dot product
print(v + w)          # elementwise addition
print(v < w)          # elementwise mask: 1.0 for true, 0.0 for false

A = me.Matrix([[1.0, 2.0], [3.0, 4.0]])
B = me.Matrix([[5.0, 6.0], [7.0, 8.0]])

print(A @ B)          # matrix multiplication
print(A.determinant())

for row in A:
    print(row)        # rows are Vector instances
```

## Validation And Exceptions

The Python API exposes custom exception classes:

```python
import matrix_engine as me

try:
    me.Matrix([[1.0, 2.0, 3.0]]).determinant()
except me.ShapeError as exc:
    print(exc)
```

Available exception types:

- `LinalgError`
- `ShapeError`
- `DimensionError`
- `IndexError`
- `EmptyMatrixError`
- `ValueError`

Validation helpers are available under `me.validation`:

```python
me.validation.square(matrix)
me.validation.same_shape(lhs, rhs)
me.validation.multiplication(lhs, rhs)
```

Most operations call validation internally, so users usually do not need to call
these helpers directly.

## Build

From the repository root:

```powershell
cmake -S cpp_math -B cpp_math/build
cmake --build cpp_math/build
```

From inside `cpp_math`:

```powershell
cmake -S . -B build
cmake --build build
```

The extension module is built into:

```text
cpp_math/matrix_engine/
```

## Install For Python Development

From inside `cpp_math`:

```powershell
pip install -e .
```

If you are working from the repository root without installing, add `cpp_math`
to `PYTHONPATH` or insert it into `sys.path`:

```python
import sys
from pathlib import Path

sys.path.insert(0, str(Path.cwd() / "cpp_math"))
```

## Tests

Build first:

```powershell
cmake --build cpp_math/build
```

Run C++ tests:

```powershell
ctest --test-dir cpp_math/build -C Debug --output-on-failure
```

Run Python tests:

```powershell
python cpp_math/tests/python/run_tests.py
```

The GitHub Actions workflow in `.github/workflows/tests.yml` runs both the C++
and Python test suites.

## Current Limitations

These methods are declared but not implemented yet:

- `Matrix.inverse()`
- `Matrix.adjugate()`
- `Matrix.rref()`
- `Matrix.rank()`
- `Vector.solve()`

They validate inputs where appropriate and then raise `ValueError`.

## License

MIT. See `LICENSE`.
