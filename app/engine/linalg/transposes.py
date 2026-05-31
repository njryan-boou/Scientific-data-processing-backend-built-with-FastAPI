import numpy as np
from app.engine.utils import validation

def transpose(matrix: list[list[float]]) -> list[list[float]]:

    arr = validation.asarray(matrix)

    try:
        transpose = np.transpose(matrix)
        
    except np.linalg.LinAlgError:
        raise ValueError("Transpose computation did not converse")
    return transpose.tolist()