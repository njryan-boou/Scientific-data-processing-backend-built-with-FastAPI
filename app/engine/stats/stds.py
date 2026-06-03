import numpy as np
from app.engine.utils import validation
from app.types import Vector

def std(data: Vector) -> float:
    
    arr = validation.asarray(data)
    
    try:
        std = np.std(arr)
        
    except np.linalg.LinAlgError:
        raise ValueError("Standard Deviation computation did not converge")
    return float(std)