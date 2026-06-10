import numpy as np
from app.engine.utils import validation
from app.types import Matrix


def determinant(matrix: Matrix) -> float:
    

    arr = validation.asarray(matrix)
    validation.validate_square(arr)

    try: 
        det = np.linalg.det(arr)
    
    except np.linalg.LinAlgError:
        raise ValueError("Determinant computation did not converge")
    return float(det)
