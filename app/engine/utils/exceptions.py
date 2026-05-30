""" Custom Errors"""

class MatrixError(Exception):
    pass


class MatrixShapeError(MatrixError):
    pass


class SingularMatrixError(MatrixError):
    pass