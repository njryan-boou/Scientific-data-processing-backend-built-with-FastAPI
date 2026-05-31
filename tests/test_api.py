from fastapi.testclient import TestClient
import numpy as np
import pytest

from app.api.main import app


client = TestClient(app)


def test_health():

    response = client.get("/health")

    assert response.status_code == 200

    assert response.json() == {
        "status": "running"
    }


def test_determinant_endpoint_success():

    response = client.post(
        "/determinant",
        json={
            "matrix": [[1, 2], [3, 4]]
        },
    )

    assert response.status_code == 200
    assert response.json()["determinant"] == pytest.approx(-2.0)


def test_determinant_endpoint_non_square_returns_400():

    response = client.post(
        "/determinant",
        json={
            "matrix": [[1, 2, 3], [4, 5, 6]]
        },
    )

    assert response.status_code == 400
    assert "square" in response.json()["detail"].lower()


def test_inverse_endpoint_success():

    response = client.post(
        "/inverse",
        json={
            "matrix": [[1, 2], [3, 4]]
        },
    )

    assert response.status_code == 200
    assert np.allclose(response.json()["inverse"], [
        [-2.0, 1.0],
        [1.5, -0.5],
    ])


def test_inverse_endpoint_singular_returns_400():

    response = client.post(
        "/inverse",
        json={
            "matrix": [[1, 2], [2, 4]]
        },
    )

    assert response.status_code == 400
    assert "singular" in response.json()["detail"].lower()


def test_transpose_endpoint_success():

    response = client.post(
        "/transpose",
        json={
            "matrix": [[1, 2, 3], [4, 5, 6]]
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "transpose": [
            [1.0, 4.0],
            [2.0, 5.0],
            [3.0, 6.0],
        ]
    }


def test_eigenvalues_endpoint_success():

    response = client.post(
        "/eigenvalues",
        json={
            "matrix": [[2, 0], [0, 3]]
        },
    )

    assert response.status_code == 200
    assert sorted(response.json()["eigenvalues"]) == [2.0, 3.0]


def test_eigenvectors_endpoint_success_shape():

    response = client.post(
        "/eigenvectors",
        json={
            "matrix": [[1, 0], [0, 1]]
        },
    )

    assert response.status_code == 200
    vecs = response.json()["eigenvectors"]
    assert len(vecs) == 2
    assert all(len(row) == 2 for row in vecs)


def test_trace_endpoint_success():

    response = client.post(
        "/trace",
        json={
            "matrix": [[1, 2], [3, 4]]
        },
    )

    assert response.status_code == 200
    assert response.json()["trace"] == 5.0


def test_matrix_validation_ragged_returns_422():

    response = client.post(
        "/determinant",
        json={
            "matrix": [[1, 2], [3]]
        },
    )

    assert response.status_code == 422