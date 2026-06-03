from pydantic import BaseModel, field_validator
from app.engine.utils import validation

from app.types import Matrix, Vector

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
    
    
class StatsRequest(BaseModel):
    
    data: Vector
    
    @field_validator("data")
    @classmethod
    def validate_data(cls, value: float) -> float:
        
        # data cannot be empty
        validation.validate_empty_array(value)
        
        return value
    
    
class EulerRequest(BaseModel):

    y0: float
    t0: float
    step_size: float
    steps: int
    
    @field_validator("steps")
    @classmethod
    def validate_steps(cls, value: int) -> int:
        if value <= 0:
            raise ValueError("Steps must be a positive integer")
        return value
    
    @field_validator("step_size")
    @classmethod
    def validate_step_size(cls, value: float) -> float:
        if value <= 0:
            raise ValueError("Step size must be a positive number")
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
    
    
class MeanResponse(BaseModel):
    
    mean: float
    
    
class StdResponse(BaseModel):
    
    std: float
    
    
class MinimumResponse(BaseModel):
    
    minimum: float
    
    
class MaximumResponse(BaseModel):
    
    maximum: float
    
    
class SummaryStatsResponse(BaseModel):
    
    mean: float
    std: float
    minimum: float
    maximum: float
    
    
class EulerResponse(BaseModel):
    
    t: Vector
    y: Vector