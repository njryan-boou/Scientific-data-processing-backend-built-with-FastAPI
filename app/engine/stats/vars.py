import numpy as np
from app.engine.utils import validation
from app.types import Vector

def variance(data: Vector) -> float:
    
    arr = validation.asarray(data)
    
    try:
        var = np.var(arr)
        
    except np.linalg.LinAlgError:
        raise ValueError("Variance computation did not converge")
    return float(var)