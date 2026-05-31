import numpy as np
from app.engine.utils import validation, exceptions
from app.types import Matrix

def inverse(matrix: Matrix) -> Matrix:

    arr = validation.asarray(matrix)
    validation.validate_square(arr)

    try:
        inv = np.linalg.inv(arr)

    except np.linalg.LinAlgError:

        raise exceptions.SingularMatrixError("Matrix is singular")

    return inv.tolist()