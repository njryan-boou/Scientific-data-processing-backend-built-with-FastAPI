from fastapi import APIRouter, HTTPException

from app.api.models import schemas

from app.engine import linalg

from app.engine.utils import exceptions

router = APIRouter()


@router.post("/determinant", response_model=schemas.DeterminantResponse)
def compute_determinant(req: schemas.MatrixRequest) -> dict[str, float]:

    result = linalg.determinant(req.matrix)

    return {
        "determinant": result
    }
    
@router.post("/inverse", response_model=schemas.InverseResponse)
def compute_inverse(req: schemas.MatrixRequest) -> dict[str, list[list[float]]]:
    try:
        result = linalg.inverse(req.matrix)
    
    except exceptions.SingularMatrixError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    
    return {
        "inverse": result
    }
    

@router.post("/transpose", response_model=schemas.TransposeResponse)
def compute_transpose(req: schemas.MatrixRequest) -> dict[str, list[list[float]]]:
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
    
    
@router.post("/eigenvalues")
def compute_eigenvalues(req: schemas.MatrixRequest) -> dict[str, list[complex]]:
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
    
    
@router.post("/eigenvectors")
def compute_eigenvectors(req: schemas.MatrixRequest) -> dict[str, list[list[complex]]]:
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