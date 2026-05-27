import numpy as np


def inverse(matrix):

    arr = np.array(matrix, dtype=float)

    try:
        inv = np.linalg.inv(arr)

    except np.linalg.LinAlgError:

        raise ValueError("Matrix is singular")

    return inv.tolist()