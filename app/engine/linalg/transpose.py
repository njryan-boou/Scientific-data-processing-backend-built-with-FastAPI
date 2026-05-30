import numpy as np
from app.engine.utils import validation

def transpose(matrix: list[list[float]]) -> list[list[float]]:

    arr = validation.asarray(matrix)

    return arr.T.tolist()