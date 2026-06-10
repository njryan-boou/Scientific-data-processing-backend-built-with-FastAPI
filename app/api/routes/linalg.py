from fastapi import APIRouter, HTTPException
import logging

import app.api.models as schemas

from app.engine import linalg

from app.engine.utils import exceptions

from app.types import Matrix


router = APIRouter()

logger = logging.getLogger(__name__)

@router.post("/determinant", response_model=schemas.DeterminantResponse,
             summary="Compute the determinant of a matrix",
             responses={
                 400: {"description": "Invalid matrix input"},
                 422: {"description": "Validation error"}
             },
             description="""
Computes the determinant of a square matrix.

Requirements:
- Matrix must be square.

Returns the determinant value.
"""
)
def compute_determinant(req: schemas.MatrixRequest) -> dict[str, float]:
    logger.info("Computing determinant")
    
    try:
        result = linalg.determinant(req.matrix)
        
    except (ValueError, exceptions.MatrixError) as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except Exception:
        logger.exception("Unexpected error while computing determinant")
        raise HTTPException(status_code=500, detail="Internal server error")

    return {
        "determinant": result
    }
    
    
@router.post("/inverse", response_model=schemas.InverseResponse,
             summary="Compute the inverse of a matrix",
             operation_id="matrix_inverse",
             responses={
                 400: {"description": "Invalid matrix input"},
                 422: {"description": "Validation error"}
             },
             description="""
Computes the inverse of a square matrix.

Requirements:
- Matrix must be square.
- Matrix must be nonsingular.

Returns the inverse matrix.
"""
)
def compute_inverse(req: schemas.MatrixRequest) -> dict[str, Matrix]:
    logger.info("Computing inverse")
    
    try:
        result = linalg.inverse(req.matrix)
    
    except exceptions.SingularMatrixError as e:
        logger.warning("Singular matrix submitted")
        
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except (ValueError, exceptions.MatrixError) as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except Exception:
        logger.exception("Unexpected error while computing inverse")
        raise HTTPException(status_code=500, detail="Internal server error")
    
    return {
        "inverse": result
    }
    


@router.post("/transpose", response_model=schemas.TransposeResponse,
             summary="Compute the transpose of a matrix",
             responses={
                 400: {"description": "Invalid matrix input"},
                 422: {"description": "Validation error"}
             },
             description="""
Computes the transpose of a matrix.

Requirements:
- Matrix can be any shape.

Returns the transposed matrix.
"""
)
def compute_transpose(req: schemas.MatrixRequest) -> dict[str, Matrix]:
    logger.info("Computing transpose")
    
    try:
        result = linalg.transpose(req.matrix)
    except (ValueError, exceptions.MatrixError) as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except Exception:
        logger.exception("Unexpected error while computing transpose")
        raise HTTPException(status_code=500, detail="Internal server error")

    return {
        "transpose": result
    }
    
    
@router.post("/eigenvalues", response_model=schemas.EigValResponse,
             summary="Compute the eigenvalues of a matrix",
             responses={
                 400: {"description": "Invalid matrix input"},
                 422: {"description": "Validation error"}
             },
             description="""
Computes the eigenvalues of a square matrix.

Requirements:
- Matrix must be square.

Returns the eigenvalues of the matrix.
"""
)
def compute_eigenvalues(req: schemas.MatrixRequest) -> dict:
    logger.info("Computing eigenvalues")
    
    try:
        result = linalg.eigenvalues(req.matrix)
    except (ValueError, exceptions.MatrixError) as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except Exception:
        logger.exception("Unexpected error while computing eigenvalues")
        raise HTTPException(status_code=500, detail="Internal server error")

    return {
        "eigenvalues": result
    }
    
    
@router.post("/eigenvectors", response_model=schemas.EigVectorResponse,
             summary="Compute the eigenvectors of a matrix",
             responses={
                 400: {"description": "Invalid matrix input"},
                 422: {"description": "Validation error"}
             },
             description="""
Computes the eigenvectors of a square matrix.

Requirements:
- Matrix must be square.

Returns the eigenvectors of the matrix.
"""
)
def compute_eigenvectors(req: schemas.MatrixRequest) -> dict:
    logger.info("Computing eigenvectors")
    
    try:
        result = linalg.eigenvectors(req.matrix)
    except (ValueError, exceptions.MatrixError) as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except Exception:
        logger.exception("Unexpected error while computing eigenvectors")
        raise HTTPException(status_code=500, detail="Internal server error")

    return {
        "eigenvectors": result
    }
    
    
@router.post("/trace", response_model=schemas.TraceResponse,
             summary="Compute the trace of a matrix",
             responses={
                 400: {"description": "Invalid matrix input"},
                 422: {"description": "Validation error"}
             },
             description="""
Computes the trace of a square matrix.

Requirements:
- Matrix must be square.

Returns the trace of the matrix.
"""
)
def compute_trace(req: schemas.MatrixRequest) -> dict[str, float]:
    logger.info("Computing trace")
    
    try:
        result = linalg.trace(req.matrix)
    except (ValueError, exceptions.MatrixError) as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except Exception:
        logger.exception("Unexpected error while computing trace")
        raise HTTPException(status_code=500, detail="Internal server error")
        
    return {
        "trace": result
    }


@router.post("/matrix-addition", response_model=schemas.MatrixResponse,
             summary="Add two matrices",
             responses={
                 400: {"description": "Invalid matrix input"},
                 422: {"description": "Validation error"}
             },
             description="""
Adds two matrices element-wise.

Requirements:
- Matrices must have the same shape.

Returns the result of adding the two matrices.
"""
)
def compute_matrix_addition(req: schemas.TwoMatrixSameShapeRequest) -> dict[str, Matrix]:
    logger.info("Computing matrix addition")
    
    try:
        result = linalg.add_matrices(req.matrix_a, req.matrix_b)
    except (ValueError, exceptions.MatrixError) as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except Exception:
        logger.exception("Unexpected error while adding matrices")
        raise HTTPException(status_code=500, detail="Internal server error")

    return {
        "result": result
    }
    
    
@router.post("/matrix-subtraction", response_model=schemas.MatrixResponse,
             summary="Subtract two matrices",
             responses={
                 400: {"description": "Invalid matrix input"},
                 422: {"description": "Validation error"}
             },
             description="""
Subtracts two matrices element-wise.

Requirements:
- Matrices must have the same shape.

Returns the result of subtracting the two matrices.
"""
)
def compute_matrix_subtraction(req: schemas.TwoMatrixSameShapeRequest) -> dict[str, Matrix]:
    logger.info("Computing matrix subtraction")
    
    try:
        result = linalg.subtract_matrices(req.matrix_a, req.matrix_b)
    except (ValueError, exceptions.MatrixError) as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except Exception:
        logger.exception("Unexpected error while subtracting matrices")
        raise HTTPException(status_code=500, detail="Internal server error")

    return {
        "result": result
    }
    
    
@router.post("/matrix-multiplication", response_model=schemas.MatrixResponse,
             summary="Multiply two matrices",
             responses={
                 400: {"description": "Invalid matrix input"},
                 422: {"description": "Validation error"}
             },
             description="""
Multiplies two matrices using standard matrix multiplication rules.

Requirements:
- Number of columns in the first matrix must match the number of rows in the second matrix.

Returns the result of multiplying the two matrices.
"""
)
def compute_matrix_multiplication(req: schemas.TwoMatrixRequest) -> dict[str, Matrix]:
    logger.info("Computing matrix multiplication")
    
    try:
        result = linalg.multiply_matrices(req.matrix_a, req.matrix_b)
    except (ValueError, exceptions.MatrixError) as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except Exception:
        logger.exception("Unexpected error while multiplying matrices")
        raise HTTPException(status_code=500, detail="Internal server error")

    return {
        "result": result
    }
    
    
@router.post("/scalar-multiply", response_model=schemas.MatrixResponse,
             summary="Multiply a matrix by a scalar",
             responses={
                 400: {"description": "Invalid matrix input"},
                 422: {"description": "Validation error"}
             },
             description="""
Multiplies a matrix by a scalar value.

Requirements:
- Matrix must be provided.
- Scalar must be provided.

Returns the result of multiplying the matrix by the scalar.
"""
)
def compute_scalar_multiply(req: schemas.ScalarMatrixRequest) -> dict[str, Matrix]:
    logger.info("Computing scalar multiplication")
    
    try:
        result = linalg.scalar_multiply(req.matrix, req.scalar)
    except (ValueError, exceptions.MatrixError) as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except Exception:
        logger.exception("Unexpected error while scalar multiplying matrix")
        raise HTTPException(status_code=500, detail="Internal server error")

    return {
        "result": result
    }
    
    
@router.post("/scalar-divide", response_model=schemas.MatrixResponse,
             summary="Divide a matrix by a scalar",
             responses={
                 400: {"description": "Invalid matrix input"},
                 422: {"description": "Validation error"}
             },
             description="""
Divides a matrix by a scalar value.

Requirements:
- Matrix must be provided.
- Scalar must be provided and non-zero.

Returns the result of dividing the matrix by the scalar.
"""
)
def compute_scalar_divide(req: schemas.ScalarMatrixRequest) -> dict[str, Matrix]:
    logger.info("Computing scalar division")
    
    try:
        result = linalg.scalar_divide(req.matrix, req.scalar)
    except (ValueError, exceptions.MatrixError) as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except Exception:
        logger.exception("Unexpected error while scalar dividing matrix")
        raise HTTPException(status_code=500, detail="Internal server error")

    return {
        "result": result
    }
    
    
@router.post("/lu-decomposition", response_model=schemas.LUResponse,
             summary="Perform LU decomposition on a matrix",
                responses={
                    400: {"description": "Invalid matrix input"},
                    422: {"description": "Validation error"}
                },
                description="""
Performs LU decomposition on a square matrix.

Requirements:
- Matrix must be square.

Returns the permutation matrix (P), lower triangular matrix (L), and upper triangular matrix (U).
"""
)
def compute_lu_decomposition(req: schemas.MatrixRequest) -> dict[str, Matrix]:
    logger.info("Computing LU decomposition")
    
    try:
        P, L, U = linalg.lu_decomposition(req.matrix)
    except (ValueError, exceptions.MatrixError) as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except Exception:
        logger.exception("Unexpected error while performing LU decomposition")
        raise HTTPException(status_code=500, detail="Internal server error")

    return {
        "P": P,
        "L": L,
        "U": U
    }
    
    
@router.post("/qr-decomposition", response_model=schemas.QRResponse,
             summary="Perform QR decomposition on a matrix",
                responses={
                    400: {"description": "Invalid matrix input"},
                    422: {"description": "Validation error"}
                },
                description="""
Performs QR decomposition on a square matrix.

Requirements:
- Matrix must be square.

Returns the orthogonal matrix (Q) and the upper triangular matrix (R).
"""
)
def compute_qr_decomposition(req: schemas.MatrixRequest) -> dict[str, Matrix]:
    logger.info("Computing QR decomposition")
    
    try:
        Q, R = linalg.qr_decomposition(req.matrix)
    except (ValueError, exceptions.MatrixError) as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except Exception:
        logger.exception("Unexpected error while performing QR decomposition")
        raise HTTPException(status_code=500, detail="Internal server error")

    return {
        "Q": Q,
        "R": R
    }
    
    
@router.post("/svd-decomposition", response_model=schemas.SVDResponse,
             summary="Perform SVD decomposition on a matrix",
                responses={
                    400: {"description": "Invalid matrix input"},
                    422: {"description": "Validation error"}
                },
                description="""
Performs Singular Value Decomposition (SVD) on a matrix.

Requirements:
- Matrix must be provided.

Returns the left singular vectors (U), singular values (S), and right singular vectors transposed (Vt).
"""
)
def compute_svd_decomposition(req: schemas.MatrixRequest) -> dict[str, Matrix]:
    logger.info("Computing SVD decomposition")
    
    try:
        U, S, Vt = linalg.svd_decomposition(req.matrix)
    except (ValueError, exceptions.MatrixError) as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except Exception:
        logger.exception("Unexpected error while performing SVD decomposition")
        raise HTTPException(status_code=500, detail="Internal server error")

    return {
        "U": U,
        "S": S,
        "Vt": Vt
    }