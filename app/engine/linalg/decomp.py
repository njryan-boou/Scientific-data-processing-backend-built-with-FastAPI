import numpy as np
from scipy.linalg import lu
from app.engine.utils import validation
from app.types import Matrix


def lu_decomposition(matrix: Matrix) -> tuple[list]:
    
    arr = validation.asarray(matrix)
    validation.validate_square(arr)

    try:
        P, L, U = lu(arr)
    
    except Exception as e:
        raise ValueError(f"LU decomposition failed: {str(e)}")
    
    return P.tolist(), L.tolist(), U.tolist()


def qr_decomposition(matrix: Matrix) -> tuple[list]:
    
    arr = validation.asarray(matrix)
    validation.validate_square(arr)

    try:
        Q, R = np.linalg.qr(arr)
    
    except np.linalg.LinAlgError:
        raise ValueError("QR decomposition did not converge")
    
    return Q.tolist(), R.tolist()


def svd_decomposition(matrix: Matrix) -> tuple[list]:
    
    arr = validation.asarray(matrix)

    try:
        U, S, Vt = np.linalg.svd(arr, full_matrices=False)
    
    except np.linalg.LinAlgError:
        raise ValueError("SVD decomposition did not converge")
    
    return U.tolist(), S.tolist(), Vt.tolist()

