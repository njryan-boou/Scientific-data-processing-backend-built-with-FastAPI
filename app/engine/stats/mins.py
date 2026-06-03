import numpy as np
from app.engine.utils import validation
from app.types import Vector

def minimum(data: Vector) -> float:
    
    arr = validation.asarray(data)
    
    try:
        min = np.min(arr)
        
    except np.linalg.LinAlgError:
        raise ValueError("Mean computation did not converge")
    return float(min)