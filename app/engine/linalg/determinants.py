import numpy as np
from app.engine.utils import validation


def determinant(matrix: list[list[float]]) -> float:
    

    arr = validation.asarray(matrix)
    validation.validate_square(matrix)

    return float(np.linalg.det(arr))