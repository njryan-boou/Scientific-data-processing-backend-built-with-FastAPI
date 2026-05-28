from pydantic import BaseModel, field_validator


class MatrixRequest(BaseModel):

    matrix: list[list[float]]

    @field_validator("matrix")
    @classmethod
    def validate_matrix(cls, value):

        # Matrix cannot be empty
        if not value:
            raise ValueError(
                "Matrix cannot be empty"
            )

        # Rows cannot be empty
        if not all(value):
            raise ValueError(
                "Matrix rows cannot be empty"
            )

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

    inverse: list[list[float]]