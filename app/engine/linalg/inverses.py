import numpy as np
from app.engine.utils import validation, exceptions

def inverse(matrix: list[list[float]]) -> list[list[float]]:

    arr = validation.asarray(matrix)
    validation.validate_square(arr)

    try:
        inv = np.linalg.inv(arr).tolist()

    except np.linalg.LinAlgError:

        raise exceptions.SingularMatrixError("Matrix is singular")

    return inv