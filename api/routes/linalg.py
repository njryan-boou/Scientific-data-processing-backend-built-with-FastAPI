from fastapi import APIRouter

from api.models.schemas import MatrixRequest

from engine.linalg import determinant


router = APIRouter()


@router.post("/determinant")
def compute_determinant(req: MatrixRequest):

    result = determinant(req.matrix)

    return {
        "determinant": result
    }