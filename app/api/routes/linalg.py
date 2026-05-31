from fastapi import APIRouter, HTTPException
import logging

from app.api.models import schemas

from app.engine import linalg

from app.engine.utils import exceptions

from app.types import Matrix

router = APIRouter()

logger = logging.getLogger(__name__)

@router.post("/determinant", response_model=schemas.DeterminantResponse)
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
    
@router.post("/inverse", response_model=schemas.InverseResponse)
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
    

@router.post("/transpose", response_model=schemas.TransposeResponse)
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
    
    
@router.post("/eigenvalues", response_model=schemas.EigValResponse)
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
    
    
@router.post("/eigenvectors", response_model=schemas.EigVectorResponse)
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
    
    
@router.post("/trace", response_model=schemas.TraceResponse)
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
"""uvicorn command:
uvicorn app.api.main:app --reload --port 8001"""