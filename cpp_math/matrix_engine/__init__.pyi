"""Python bindings for the C++ matrix engine using pybind11."""

from typing import Iterable, Iterator, overload

__version__: str
__author__: str
__description__: str


class LinalgError(RuntimeError):
    """Base exception for matrix_engine errors."""


class ShapeError(LinalgError):
    """Raised when a matrix/vector shape is invalid for an operation."""


class DimensionError(LinalgError):
    """Raised when dimensions are incompatible for an operation."""


class IndexError(LinalgError):
    """Raised when an index is out of bounds."""


class EmptyMatrixError(LinalgError):
    """Raised when an operation requires a non-empty matrix."""


class ValueError(LinalgError):
    """Raised when a value is invalid for an operation."""


class _ValidationModule:
    def require(self, condition: bool, message: str) -> None:
        """Raise ValueError with message when condition is false."""
        ...

    def row(self, index: int, rows: int) -> None:
        """Validate that a row index is within [0, rows)."""
        ...

    def column(self, index: int, cols: int) -> None:
        """Validate that a column index is within [0, cols)."""
        ...

    def not_empty(self, matrix: "Matrix") -> None:
        """Validate that a matrix has at least one row and one column."""
        ...

    def square(self, matrix: "Matrix") -> None:
        """Validate that a matrix has the same number of rows and columns."""
        ...

    def same_shape(self, lhs: "Matrix", rhs: "Matrix") -> None:
        """Validate that two matrices have identical shapes."""
        ...

    def multiplication(self, lhs: "Matrix", rhs: "Matrix") -> None:
        """Validate that two matrices are compatible for matrix multiplication."""
        ...

    def positive_dimension(self, value: int, name: str) -> None:
        """Validate that a named dimension is greater than zero."""
        ...

    def reshape(self, current: int, requested: int) -> None:
        """Validate that a reshape preserves the total element count."""
        ...


validation: _ValidationModule


class Vector:
    """A mathematical vector backed by the C++ engine."""

    @overload
    def __init__(self, size: int) -> None:
        """Create a zero-filled vector with size elements."""
        ...

    @overload
    def __init__(self, values: Iterable[float]) -> None:
        """Create a vector from a sequence of numeric values."""
        ...

    def size(self) -> int:
        """Return the number of elements in the vector."""
        ...

    def dot(self, other: "Vector") -> float:
        """Return the dot product with another vector."""
        ...

    def magnitude(self) -> float:
        """Return the Euclidean magnitude of the vector."""
        ...

    def normalize(self) -> "Vector":
        """Return a normalized copy of the vector."""
        ...

    def cross(self, other: "Vector") -> "Vector":
        """Return the 3D cross product with another vector."""
        ...

    def solve(self, A: "Matrix") -> "Vector":
        """Solve the linear system A*x = self. Currently not implemented."""
        ...

    def __len__(self) -> int:
        """Return the number of elements in the vector."""
        ...

    def __iter__(self) -> Iterator[float]:
        """Iterate over vector values."""
        ...

    def __getitem__(self, index: int) -> float:
        """Return the value at index."""
        ...

    def __setitem__(self, index: int, value: float) -> None:
        """Set the value at index."""
        ...

    def __add__(self, other: "Vector") -> "Vector":
        """Return the elementwise sum of two vectors."""
        ...

    def __radd__(self, other: "Vector") -> "Vector":
        """Return the elementwise sum of two vectors."""
        ...

    def __sub__(self, other: "Vector") -> "Vector":
        """Return the elementwise difference of two vectors."""
        ...

    def __rsub__(self, other: "Vector") -> "Vector":
        """Return other minus this vector elementwise."""
        ...

    def __mul__(self, other: "Vector | float") -> "Vector":
        """Return elementwise vector product or scalar multiplication."""
        ...

    @overload
    def __rmul__(self, other: "Vector") -> "Vector":
        """Return the elementwise product of two vectors."""
        ...

    @overload
    def __rmul__(self, other: float) -> "Vector":
        """Return this vector multiplied by a scalar."""
        ...

    def __truediv__(self, other: "Vector | float") -> "Vector":
        """Return elementwise vector quotient or scalar division."""
        ...

    @overload
    def __rtruediv__(self, other: "Vector") -> "Vector":
        """Return other divided by this vector elementwise."""
        ...

    @overload
    def __rtruediv__(self, other: float) -> "Vector":
        """Return scalar divided by this vector elementwise."""
        ...

    def __neg__(self) -> "Vector":
        """Return the negated vector."""
        ...

    def __eq__(self, other: "Vector") -> "Vector":
        """Return an elementwise equality mask as a vector of 1.0 and 0.0."""
        ...

    def __ne__(self, other: "Vector") -> "Vector":
        """Return an elementwise inequality mask as a vector of 1.0 and 0.0."""
        ...

    def __lt__(self, other: "Vector") -> "Vector":
        """Return an elementwise less-than mask as a vector of 1.0 and 0.0."""
        ...

    def __le__(self, other: "Vector") -> "Vector":
        """Return an elementwise less-than-or-equal mask as a vector of 1.0 and 0.0."""
        ...

    def __gt__(self, other: "Vector") -> "Vector":
        """Return an elementwise greater-than mask as a vector of 1.0 and 0.0."""
        ...

    def __ge__(self, other: "Vector") -> "Vector":
        """Return an elementwise greater-than-or-equal mask as a vector of 1.0 and 0.0."""
        ...

    def __and__(self, other: "Vector") -> "Vector":
        """Return an elementwise logical-and mask as a vector of 1.0 and 0.0."""
        ...

    def __rand__(self, other: "Vector") -> "Vector":
        """Return an elementwise logical-and mask as a vector of 1.0 and 0.0."""
        ...

    def __or__(self, other: "Vector") -> "Vector":
        """Return an elementwise logical-or mask as a vector of 1.0 and 0.0."""
        ...

    def __ror__(self, other: "Vector") -> "Vector":
        """Return an elementwise logical-or mask as a vector of 1.0 and 0.0."""
        ...

    def __xor__(self, other: "Vector") -> "Vector":
        """Return an elementwise logical-xor mask as a vector of 1.0 and 0.0."""
        ...

    def __rxor__(self, other: "Vector") -> "Vector":
        """Return an elementwise logical-xor mask as a vector of 1.0 and 0.0."""
        ...

    def __invert__(self) -> "Vector":
        """Return an elementwise logical-not mask as a vector of 1.0 and 0.0."""
        ...

    def __iadd__(self, other: "Vector") -> "Vector":
        """Add another vector into this vector elementwise."""
        ...

    def __isub__(self, other: "Vector") -> "Vector":
        """Subtract another vector from this vector elementwise."""
        ...

    def __imul__(self, other: "Vector | float") -> "Vector":
        """Multiply this vector by another vector elementwise or by a scalar."""
        ...

    def __itruediv__(self, other: "Vector | float") -> "Vector":
        """Divide this vector by another vector elementwise or by a scalar."""
        ...

    @overload
    def __matmul__(self, other: "Vector") -> float:
        """Return the dot product when used as vector @ vector."""
        ...

    @overload
    def __matmul__(self, other: "Matrix") -> "Vector":
        """Return vector-matrix multiplication when used as vector @ matrix."""
        ...

    def __contains__(self, value: float) -> bool:
        """Return True if the vector contains value."""
        ...

    def __repr__(self) -> str:
        """Return the string representation of the vector."""
        ...


class Matrix:
    """A mathematical matrix backed by the C++ engine."""

    @overload
    def __init__(self, rows: int, cols: int) -> None:
        """Create a zero-filled matrix with the given row and column counts."""
        ...

    @overload
    def __init__(self, values: Iterable[Iterable[float]]) -> None:
        """Create a matrix from a rectangular nested sequence of numeric values."""
        ...

    @property
    def rows(self) -> int:
        """Number of matrix rows."""
        ...

    @property
    def cols(self) -> int:
        """Number of matrix columns."""
        ...

    @property
    def shape(self) -> tuple[int, int]:
        """Matrix shape as (rows, cols)."""
        ...

    def matmul(self, other: "Matrix") -> "Matrix":
        """Return matrix multiplication with another matrix."""
        ...

    def matvec(self, vec: Vector) -> Vector:
        """Return matrix-vector multiplication."""
        ...

    def vecmat(self, vec: Vector) -> Vector:
        """Return vector-matrix multiplication using the supplied left-side vector."""
        ...

    def transpose(self) -> "Matrix":
        """Return the transposed matrix."""
        ...

    def determinant(self) -> float:
        """Return the determinant for a supported square matrix."""
        ...

    def inverse(self) -> "Matrix":
        """Return the inverse matrix. Currently not implemented."""
        ...

    def adjugate(self) -> "Matrix":
        """Return the adjugate matrix. Currently not implemented."""
        ...

    def rref(self) -> "Matrix":
        """Return the reduced row echelon form. Currently not implemented."""
        ...

    def rank(self) -> int:
        """Return the matrix rank. Currently not implemented."""
        ...

    def __len__(self) -> int:
        """Return the number of matrix rows."""
        ...

    def __iter__(self) -> Iterator[Vector]:
        """Iterate over matrix rows as Vector instances."""
        ...

    def __getitem__(self, index: tuple[int, int]) -> float:
        """Return the value at (row, column)."""
        ...

    def __setitem__(self, index: tuple[int, int], value: float) -> None:
        """Set the value at (row, column)."""
        ...

    def __add__(self, other: "Matrix") -> "Matrix":
        """Return the elementwise sum of two matrices."""
        ...

    def __radd__(self, other: "Matrix") -> "Matrix":
        """Return the elementwise sum of two matrices."""
        ...

    def __sub__(self, other: "Matrix") -> "Matrix":
        """Return the elementwise difference of two matrices."""
        ...

    def __rsub__(self, other: "Matrix") -> "Matrix":
        """Return other minus this matrix elementwise."""
        ...

    def __mul__(self, other: "Matrix | float") -> "Matrix":
        """Return elementwise matrix product or scalar multiplication."""
        ...

    @overload
    def __rmul__(self, other: "Matrix") -> "Matrix":
        """Return the elementwise product of two matrices."""
        ...

    @overload
    def __rmul__(self, other: float) -> "Matrix":
        """Return this matrix multiplied by a scalar."""
        ...

    def __truediv__(self, other: "Matrix | float") -> "Matrix":
        """Return elementwise matrix quotient or scalar division."""
        ...

    @overload
    def __rtruediv__(self, other: "Matrix") -> "Matrix":
        """Return other divided by this matrix elementwise."""
        ...

    @overload
    def __rtruediv__(self, other: float) -> "Matrix":
        """Return scalar divided by this matrix elementwise."""
        ...

    def __neg__(self) -> "Matrix":
        """Return the negated matrix."""
        ...

    def __eq__(self, other: "Matrix") -> "Matrix":
        """Return an elementwise equality mask as a matrix of 1.0 and 0.0."""
        ...

    def __ne__(self, other: "Matrix") -> "Matrix":
        """Return an elementwise inequality mask as a matrix of 1.0 and 0.0."""
        ...

    def __lt__(self, other: "Matrix") -> "Matrix":
        """Return an elementwise less-than mask as a matrix of 1.0 and 0.0."""
        ...

    def __le__(self, other: "Matrix") -> "Matrix":
        """Return an elementwise less-than-or-equal mask as a matrix of 1.0 and 0.0."""
        ...

    def __gt__(self, other: "Matrix") -> "Matrix":
        """Return an elementwise greater-than mask as a matrix of 1.0 and 0.0."""
        ...

    def __ge__(self, other: "Matrix") -> "Matrix":
        """Return an elementwise greater-than-or-equal mask as a matrix of 1.0 and 0.0."""
        ...

    def __and__(self, other: "Matrix") -> "Matrix":
        """Return an elementwise logical-and mask as a matrix of 1.0 and 0.0."""
        ...

    def __rand__(self, other: "Matrix") -> "Matrix":
        """Return an elementwise logical-and mask as a matrix of 1.0 and 0.0."""
        ...

    def __or__(self, other: "Matrix") -> "Matrix":
        """Return an elementwise logical-or mask as a matrix of 1.0 and 0.0."""
        ...

    def __ror__(self, other: "Matrix") -> "Matrix":
        """Return an elementwise logical-or mask as a matrix of 1.0 and 0.0."""
        ...

    def __xor__(self, other: "Matrix") -> "Matrix":
        """Return an elementwise logical-xor mask as a matrix of 1.0 and 0.0."""
        ...

    def __rxor__(self, other: "Matrix") -> "Matrix":
        """Return an elementwise logical-xor mask as a matrix of 1.0 and 0.0."""
        ...

    def __invert__(self) -> "Matrix":
        """Return an elementwise logical-not mask as a matrix of 1.0 and 0.0."""
        ...

    def __iadd__(self, other: "Matrix") -> "Matrix":
        """Add another matrix into this matrix elementwise."""
        ...

    def __isub__(self, other: "Matrix") -> "Matrix":
        """Subtract another matrix from this matrix elementwise."""
        ...

    def __imul__(self, other: "Matrix | float") -> "Matrix":
        """Multiply this matrix by another matrix elementwise or by a scalar."""
        ...

    def __itruediv__(self, other: "Matrix | float") -> "Matrix":
        """Divide this matrix by another matrix elementwise or by a scalar."""
        ...

    @overload
    def __matmul__(self, other: "Matrix") -> "Matrix":
        """Return matrix multiplication when used as matrix @ matrix."""
        ...

    @overload
    def __matmul__(self, other: Vector) -> Vector:
        """Return matrix-vector multiplication when used as matrix @ vector."""
        ...

    def __contains__(self, value: float) -> bool:
        """Return True if the matrix contains value."""
        ...

    def __repr__(self) -> str:
        """Return the string representation of the matrix."""
        ...
