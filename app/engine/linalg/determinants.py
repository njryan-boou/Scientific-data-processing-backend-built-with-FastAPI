import numpy as np


def determinant(matrix):
    

    arr = np.array(matrix, dtype=np.float64)

    return float(np.linalg.det(arr))