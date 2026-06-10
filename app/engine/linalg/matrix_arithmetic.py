from app.engine.utils import validation
from app.types import Matrix


def add_matrices(matrix_a: Matrix, matrix_b: Matrix) -> Matrix:

    arr_a = validation.asarray(matrix_a)
    arr_b = validation.asarray(matrix_b)

    validation.validate_same_shape(arr_a, arr_b)

    result = arr_a + arr_b
    return result.tolist()


def subtract_matrices(matrix_a: Matrix, matrix_b: Matrix) -> Matrix:

    arr_a = validation.asarray(matrix_a)
    arr_b = validation.asarray(matrix_b)

    validation.validate_same_shape(arr_a, arr_b)

    result = arr_a - arr_b
    return result.tolist()


def multiply_matrices(matrix_a: Matrix, matrix_b: Matrix) -> Matrix:

    arr_a = validation.asarray(matrix_a)
    arr_b = validation.asarray(matrix_b)

    if arr_a.shape[1] != arr_b.shape[0]:
        raise ValueError(
            "Number of columns in Matrix A must match number of rows in Matrix B"
        )

    result = arr_a @ arr_b
    return result.tolist()


def scalar_multiply(matrix: Matrix, scalar: float) -> Matrix:

    arr = validation.asarray(matrix)
    result = arr * scalar
    return result.tolist()


def scalar_divide(matrix: Matrix, scalar: float) -> Matrix:

    if scalar == 0:
        raise ValueError("Cannot divide by zero")

    arr = validation.asarray(matrix)
    result = arr / scalar
    return result.tolist()



