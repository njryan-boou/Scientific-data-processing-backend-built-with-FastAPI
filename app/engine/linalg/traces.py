import numpy as np
from app.engine.utils import validation
from app.types import Matrix

def trace(matrix: Matrix) -> float:
    arr = validation.asarray(matrix)
    validation.validate_square(arr)
    
    try:
        trace = np.linalg.trace(arr)
        
    except np.linalg.LinAlgError:
        raise ValueError("trace computation did not converge")
    return float(trace)