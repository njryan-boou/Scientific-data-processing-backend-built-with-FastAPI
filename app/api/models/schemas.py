from pydantic import BaseModel, field_validator
from app.engine.utils import validation

from app.types import Matrix

class MatrixRequest(BaseModel):

    matrix: Matrix

    @field_validator("matrix")
    @classmethod
    def validate_matrix(cls, value: float) -> float:

        # Matrix cannot be empty
        validation.validate_empty_array(value)

        # Rows cannot be empty
        validation.validate_empty_matrix_rows(value)

        # Ensure rectangular matrix
        validation.validate_rectangular(value)

        return value
    
    

class DeterminantResponse(BaseModel):

    determinant: float
    
    
class InverseResponse(BaseModel):

    inverse: Matrix
    
    
class TransposeResponse(BaseModel):

    transpose: Matrix
    
    
class EigValResponse(BaseModel):
    eigenvalues: list[complex | float]


class EigVectorResponse(BaseModel):
    eigenvectors: list[list[complex | float]]


class TraceResponse(BaseModel):
    trace: float