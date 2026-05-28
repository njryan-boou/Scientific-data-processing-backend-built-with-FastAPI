from fastapi import APIRouter

from app.api.models.schemas import ( 
                                    MatrixRequest, 
                                    DeterminantResponse,
                                    InverseResponse,
)

from app.engine.linalg import determinant, inverse


router = APIRouter()


@router.post("/determinant", response_model=DeterminantResponse)
def compute_determinant(req: MatrixRequest):

    result = determinant(req.matrix)

    return {
        "determinant": result
    }
    
@router.post("/inverse", response_model=InverseResponse)
def compute_inverse(req: MatrixRequest):
    
    result = inverse(req.matrix)
    
    return {
        "inverse": result
    }