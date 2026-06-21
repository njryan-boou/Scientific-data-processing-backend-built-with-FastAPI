from pydantic import BaseModel

from app.types import Matrix, Vector


class MatrixResponse(BaseModel):
    result: Matrix


class InverseResponse(BaseModel):
    inverse: Matrix


class TransposeResponse(BaseModel):
    transpose: Matrix


class EigValResponse(BaseModel):
    eigenvalues: list[float | complex]


class EigVectorResponse(BaseModel):
    eigenvectors: list[list[float | complex]]


class DeterminantResponse(BaseModel):
    determinant: float


class TraceResponse(BaseModel):
    trace: float
    
    
class LUResponse(BaseModel):
    P: Matrix
    L: Matrix
    U: Matrix
    
    
class QRResponse(BaseModel):
    Q: Matrix
    R: Matrix
    
    
class SVDResponse(BaseModel):
    U: Matrix
    S: Vector
    Vt: Matrix


class MeanResponse(BaseModel):
    mean: float


class StdResponse(BaseModel):
    std: float


class VarianceResponse(BaseModel):
    variance: float


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
    
    
class RungeKuttaResponse(BaseModel):
    t: Vector
    y: Vector
