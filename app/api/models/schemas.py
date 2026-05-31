from pydantic import BaseModel, field_validator
from app.engine.utils import validation

from app.types import MatrixType

class MatrixRequest(BaseModel):

    matrix: MatrixType

    @field_validator("matrix")
    @classmethod
    def validate_matrix(cls, value):

        # Matrix cannot be empty
        validation.validate_empty_array(value)

        # Rows cannot be empty
        validation.validate_empty_matrix_rows(value)

        # Ensure rectangular matrix
        row_lengths = {
            len(row) for row in value
        }

        if len(row_lengths) != 1:
            raise ValueError(
                "All matrix rows must have equal length"
            )

        return value
    
    

class DeterminantResponse(BaseModel):

    determinant: float
    
    
class InverseResponse(BaseModel):

    inverse: MatrixType
    
    
class TransposeResponse(BaseModel):

    transpose: MatrixType
    
    
class EigValResponse(BaseModel):
    pass


class EigVectorResponse(BaseModel):
    pass


class TraceResponse(BaseModel):
    pass