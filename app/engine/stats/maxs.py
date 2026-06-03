import numpy as np
from app.engine.utils import validation
from app.types import Vector

def maximum(data: Vector) -> float:
    
    arr = validation.asarray(data)
    
    try:
        max = np.max(arr)
        
    except np.linalg.LinAlgError:
        raise ValueError("Mean computation did not converge")
    return float(max)