import numpy as np
from app.engine.utils import validation
from app.types import Vector

def mean(data: Vector) -> float:
    
    arr = validation.asarray(data)
    
    try:
        mean = np.mean(arr)
        
    except np.linalg.LinAlgError:
        raise ValueError("Mean computation did not converge")
    return float(mean)