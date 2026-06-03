from fastapi import APIRouter, HTTPException
import logging

from app.api.models import schemas

from app.engine import linalg

from app.engine.utils import exceptions

from app.types import Matrix

router = APIRouter()

logger = logging.getLogger(__name__)


@router.post("/determinant", response_model=schemas.DeterminantResponse,
             summary="Compute the determinant of a matrix",
             description="Returns the determinant of the input matrix. The determinant is a scalar value that can be computed from the elements of a square matrix.")
def compute_determinant(req: schemas.MatrixRequest) -> dict[str, float]:
    logger.info("Computing determinant")
    
    try:
        result = linalg.determinant(req.matrix)
        
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    return {
        "determinant": result
    }
    
    
@router.post("/inverse", response_model=schemas.InverseResponse,
             summary="Compute the inverse of a matrix",
             description="Returns the inverse of the input matrix. The inverse is a matrix that, when multiplied with the original matrix, yields the identity matrix.")
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
    
    return {
        "inverse": result
    }
    


@router.post("/transpose", response_model=schemas.TransposeResponse,
             summary="Compute the transpose of a matrix",
             description="Returns the transpose of the input matrix. The transpose is obtained by swapping the rows and columns of the original matrix.")
def compute_transpose(req: schemas.MatrixRequest) -> dict[str, Matrix]:
    logger.info("Computing transpose")
    
    try:
        result = linalg.transpose(req.matrix)
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    return {
        "transpose": result
    }
    
    
@router.post("/eigenvalues", response_model=schemas.EigValResponse,
             summary="Compute the eigenvalues of a matrix",
             description="Returns the eigenvalues of the input matrix. Eigenvalues are scalars associated with a square matrix that provide insights into its properties.")
def compute_eigenvalues(req: schemas.MatrixRequest) -> dict:
    logger.info("Computing eigenvalues")
    
    try:
        result = linalg.eigenvalues(req.matrix)
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    return {
        "eigenvalues": result
    }
    
    
@router.post("/eigenvectors", response_model=schemas.EigVectorResponse,
             summary="Compute the eigenvectors of a matrix",
             description="Returns the eigenvectors of the input matrix. Eigenvectors are vectors associated with a square matrix that provide insights into its properties.")
def compute_eigenvectors(req: schemas.MatrixRequest) -> dict:
    logger.info("Computing eigenvectors")
    
    try:
        result = linalg.eigenvectors(req.matrix)
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    return {
        "eigenvectors": result
    }
    
    
@router.post("/trace", response_model=schemas.TraceResponse,
             summary="Compute the trace of a matrix",
             description="Returns the trace of the input matrix. The trace is the sum of the elements on the main diagonal of a square matrix.")
def compute_trace(req: schemas.MatrixRequest) -> dict[str, float]:
    logger.info("Computing trace")
    
    try:
        result = linalg.trace(req.matrix)
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
        
    return {
        "trace": result
    }
