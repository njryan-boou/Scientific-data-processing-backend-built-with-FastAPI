from pydantic import BaseModel


class MatrixRequest(BaseModel):

    matrix: list[list[float]]