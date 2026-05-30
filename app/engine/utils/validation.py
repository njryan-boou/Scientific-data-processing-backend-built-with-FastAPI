import numpy as np

from app.engine.utils import exceptions

def asarray(arr: list | np.ndarray) -> np.ndarray:
    return np.asarray(arr, dtype=np.float64)


def validate_square(arr: np.ndarray) -> np.ndarray:
    if arr.shape[0] == arr.shape[1]:
        raise exceptions.MatrixShapeError("Matrix must be a square")
    
    
def validate_empty_array(value: float):
    if not value:
        raise TypeError("Matrix cannot be empty")
    

def validate_empty_matrix_rows(value: float):
    if not all(value):
            raise ValueError("Matrix rows cannot be empty")