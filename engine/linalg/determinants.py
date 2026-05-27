import numpy as np


def determinant(matrix):

    arr = np.array(matrix, dtype=float)

    return float(np.linalg.det(arr))