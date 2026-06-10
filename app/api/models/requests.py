from pydantic import BaseModel, field_validator

from app.engine.utils import validation
from app.types import Matrix, Vector

from .configs import (
    euler_config,
    matrix_2_config,
    matrix_config,
    scalar_matrix_config,
    vector_config,
)


class MatrixRequest(BaseModel):
    matrix: Matrix

    model_config = matrix_config

    @field_validator("matrix")
    @classmethod
    def validate_matrix(cls, value: float) -> float:
        validation.validate_empty_array(value)
        validation.validate_empty_matrix_rows(value)
        validation.validate_rectangular(value)
        return value


class VectorRequest(BaseModel):
    vector: Vector

    model_config = vector_config

    @field_validator("vector")
    @classmethod
    def validate_vector(cls, value: float) -> float:
        validation.validate_empty_array(value)
        return value


class TwoMatrixRequest(BaseModel):
    matrix_a: Matrix
    matrix_b: Matrix

    model_config = matrix_2_config

    @field_validator("matrix_a", "matrix_b")
    @classmethod
    def validate_matrices(cls, value: Matrix) -> Matrix:
        validation.validate_empty_array(value)
        validation.validate_empty_matrix_rows(value)
        validation.validate_rectangular(value)
        return value

    @field_validator("matrix_b")
    @classmethod
    def validate_compatibility(cls, value: float, info) -> float:
        matrix_a = info.data.get("matrix_a")

        if matrix_a is None:
            raise ValueError("Matrix A must be provided")

        if len(matrix_a[0]) != len(value):
            raise ValueError("Number of columns in Matrix A must match number of rows in Matrix B")

        return value


class TwoMatrixSameShapeRequest(BaseModel):
    matrix_a: Matrix
    matrix_b: Matrix

    model_config = matrix_2_config

    @field_validator("matrix_a", "matrix_b")
    @classmethod
    def validate_matrices(cls, value: Matrix) -> Matrix:
        validation.validate_empty_array(value)
        validation.validate_empty_matrix_rows(value)
        validation.validate_rectangular(value)
        return value

    @field_validator("matrix_b")
    @classmethod
    def validate_same_shape(cls, value: Matrix, info) -> Matrix:
        matrix_a = info.data.get("matrix_a")

        if matrix_a is None:
            raise ValueError("Matrix A must be provided")

        if len(matrix_a) != len(value) or len(matrix_a[0]) != len(value[0]):
            raise ValueError("Matrices must have the same shape")

        return value


class ScalarMatrixRequest(BaseModel):
    matrix: Matrix
    scalar: float

    model_config = scalar_matrix_config

    @field_validator("matrix")
    @classmethod
    def validate_matrix(cls, value: Matrix) -> Matrix:
        validation.validate_empty_array(value)
        validation.validate_empty_matrix_rows(value)
        validation.validate_rectangular(value)
        return value


class EulerRequest(BaseModel):
    y0: float
    t0: float
    step_size: float
    steps: int

    model_config = euler_config

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
