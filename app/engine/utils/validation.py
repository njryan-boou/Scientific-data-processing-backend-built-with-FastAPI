import numpy as np

from app.engine.utils import exceptions

def asarray(arr: list | np.ndarray) -> np.ndarray:
    validate_empty_array(arr)
    return np.asarray(arr, dtype=np.float64)


def validate_square(arr: np.ndarray) -> np.ndarray:
    if arr.ndim != 2 or arr.shape[0] != arr.shape[1]:
        raise exceptions.MatrixShapeError("Matrix must be a square")
    return arr
    
    
def validate_empty_array(value: float):
    if not value:
        raise ValueError("Array cannot be empty")
    

def validate_empty_matrix_rows(value: float):
    if not all(value):
            raise ValueError("Matrix rows cannot be empty")
        
        
def validate_rectangular(value: float):
    row_lengths = {
            len(row) for row in value
        }

    if len(row_lengths) != 1:
        raise ValueError(
            "All matrix rows must have equal length"
        )