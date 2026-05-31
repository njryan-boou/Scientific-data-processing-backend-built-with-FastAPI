import numpy as np
from app.engine.utils import validation

def trace(matrix):
    arr = validation.asarray(matrix)
    validation.validate_square(matrix)
    
    try:
        trace = np.linalg.trace(arr)
        
    except np.linalg.LinAlgError:
        raise ValueError("trace computation did not converge")
    return float(trace)