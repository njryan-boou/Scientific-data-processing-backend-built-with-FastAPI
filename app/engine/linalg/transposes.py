import numpy as np
from app.engine.utils import validation
from app.types import Matrix
import matrix_engine as me

def transpose(matrix: Matrix) -> Matrix:

    arr = validation.asarray(matrix)

    try:
        transpose = np.transpose(arr)
    
    except np.linalg.LinAlgError:
        raise ValueError("Transpose computation did not converge")
    return transpose.tolist()