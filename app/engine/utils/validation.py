import numpy as np
from collections.abc import Sequence

from app.engine.utils import exceptions


def asarray(arr: Sequence | np.ndarray) -> np.ndarray:
    validate_empty_array(arr)
    return np.asarray(arr, dtype=np.float64)


def validate_square(arr: np.ndarray) -> np.ndarray:
    if arr.ndim != 2 or arr.shape[0] != arr.shape[1]:
        raise exceptions.MatrixShapeError("Matrix must be a square")
    return arr


def validate_empty_array(value: Sequence | np.ndarray) -> None:
    if not value:
        raise ValueError("Array cannot be empty")


def validate_empty_matrix_rows(value: Sequence[Sequence]) -> None:
    if not all(value):
        raise ValueError("Matrix rows cannot be empty")


def validate_rectangular(value: Sequence[Sequence]) -> None:
    row_lengths = {
        len(row) for row in value
    }

    if len(row_lengths) != 1:
        raise ValueError(
            "All matrix rows must have equal length"
        )


def validate_same_shape(arr_a: np.ndarray, arr_b: np.ndarray) -> None:
    if arr_a.shape != arr_b.shape:
        raise exceptions.MatrixShapeError("Matrices must have the same shape")