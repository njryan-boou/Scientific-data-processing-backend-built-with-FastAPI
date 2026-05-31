from app.engine import linalg
from app.engine.utils import exceptions
import pytest
import numpy as np

# determinant tests

def test_determinant_2x2():

    matrix = [
        [1, 2],
        [3, 4]
    ]

    result = linalg.determinant(matrix)

    assert result == pytest.approx(-2.0)
    
    
def test_determinant_identity():

    matrix = [
        [1, 0],
        [0, 1]
    ]

    assert linalg.determinant(matrix) == 1.0
    
    
def test_determinant_zero():

    matrix = [
        [0, 0],
        [0, 0]
    ]

    assert linalg.determinant(matrix) == 0.0
    
    
def test_determinant_non_square():

    matrix = [
        [1, 2, 3],
        [4, 5, 6]
    ]

    with pytest.raises(exceptions.MatrixShapeError):

        linalg.determinant(matrix)
        
        
# inverse tests

def test_inverse_2x2():

    matrix = [
        [1, 2],
        [3, 4]
    ]

    result = linalg.inverse(matrix)

    expected = [
        [-2.0, 1.0],
        [1.5, -0.5]
    ]

    assert np.allclose(result, expected)
    
    
def test_inverse_identity():

    matrix = [
        [1, 0],
        [0, 1]
    ]

    result = linalg.inverse(matrix)

    expected = [
        [1.0, 0.0],
        [0.0, 1.0]
    ]

    assert result == expected


def test_inverse_singular_matrix_raises():

    matrix = [
        [1, 2],
        [2, 4]
    ]

    with pytest.raises(exceptions.SingularMatrixError):
        linalg.inverse(matrix)


# transpose tests

def test_transpose_rectangular_matrix():

    matrix = [
        [1, 2, 3],
        [4, 5, 6]
    ]

    result = linalg.transpose(matrix)

    assert result == [
        [1.0, 4.0],
        [2.0, 5.0],
        [3.0, 6.0],
    ]


def test_transpose_square_matrix():

    matrix = [
        [1, 2],
        [3, 4]
    ]

    assert linalg.transpose(matrix) == [
        [1.0, 3.0],
        [2.0, 4.0],
    ]


# trace tests

def test_trace_square_matrix():

    matrix = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9],
    ]

    assert linalg.trace(matrix) == 15.0


def test_trace_non_square_raises():

    matrix = [
        [1, 2, 3],
        [4, 5, 6]
    ]

    with pytest.raises(exceptions.MatrixShapeError):
        linalg.trace(matrix)


# eigenvalue/eigenvector tests

def test_eigenvalues_diagonal_matrix():

    matrix = [
        [2, 0],
        [0, 3],
    ]

    result = linalg.eigenvalues(matrix)

    assert sorted(result) == [2.0, 3.0]


def test_eigenvalues_non_square_raises():

    matrix = [
        [1, 2, 3],
        [4, 5, 6]
    ]

    with pytest.raises(exceptions.MatrixShapeError):
        linalg.eigenvalues(matrix)


def test_eigenvectors_for_identity_columns_are_basis():

    matrix = [
        [1, 0],
        [0, 1]
    ]

    result = linalg.eigenvectors(matrix)
    arr = np.asarray(result)

    assert arr.shape == (2, 2)
    assert np.allclose(arr.T @ arr, np.eye(2), atol=1e-7)
    assert np.allclose(np.abs(arr), np.eye(2), atol=1e-7)


def test_eigenvectors_non_square_raises():

    matrix = [
        [1, 2, 3],
        [4, 5, 6]
    ]

    with pytest.raises(exceptions.MatrixShapeError):
        linalg.eigenvectors(matrix)