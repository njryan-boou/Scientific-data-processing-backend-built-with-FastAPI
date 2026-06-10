import numpy as np
from app.engine.utils import validation
from app.types import Matrix, Eigenvalues, Eigenvectors

def eigenvalues(matrix: Matrix) -> Eigenvalues:
    arr = validation.asarray(matrix)
    validation.validate_square(arr)

    try:
        vals = np.linalg.eigvals(arr)
    except np.linalg.LinAlgError:
        raise ValueError("Eigenvalue computation did not converge")
    
    return vals.tolist()

def eigenvectors(matrix: Matrix) -> Eigenvectors:
    arr = validation.asarray(matrix)
    validation.validate_square(arr)

    try:
        _, vecs = np.linalg.eig(arr)
    except np.linalg.LinAlgError:
        raise ValueError("Eigenvector computation did not converge")

    return vecs.tolist()