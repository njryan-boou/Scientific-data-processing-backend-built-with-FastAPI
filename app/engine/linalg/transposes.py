import numpy as np
from app.engine.utils import validation
from app.types import Matrix

def transpose(matrix: Matrix) -> Matrix:

    arr = validation.asarray(matrix)

    try:
        transpose = np.transpose(arr)
    
    except np.linalg.LinAlgError:
        raise ValueError("Transpose computation did not converge")
    return transpose.tolist()