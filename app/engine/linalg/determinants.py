import numpy as np
from app.engine.utils import validation


def determinant(matrix: list[list[float]]) -> float:
    

    arr = validation.asarray(matrix)
    validation.validate_square(matrix)

    try: 
        det = np.linalg.det(arr)
    
    except np.linalg.LinAlgError:
        raise ValueError("Determinant computation did not converge")
    return float(det)