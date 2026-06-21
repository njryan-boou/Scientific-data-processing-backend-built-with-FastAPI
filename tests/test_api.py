from fastapi.testclient import TestClient
import numpy as np
import pytest
from uuid import uuid4

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
        "/linalg/determinant",
        json={
            "matrix": [[1, 2], [3, 4]]
        },
    )

    assert response.status_code == 200
    assert response.json()["determinant"] == pytest.approx(-2.0)


def test_determinant_endpoint_non_square_returns_400():

    response = client.post(
        "/linalg/determinant",
        json={
            "matrix": [[1, 2, 3], [4, 5, 6]]
        },
    )

    assert response.status_code == 400
    assert "square" in response.json()["detail"].lower()


def test_inverse_endpoint_success():

    response = client.post(
        "/linalg/inverse",
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
        "/linalg/inverse",
        json={
            "matrix": [[1, 2], [2, 4]]
        },
    )

    assert response.status_code == 400
    assert "singular" in response.json()["detail"].lower()


def test_transpose_endpoint_success():

    response = client.post(
        "/linalg/transpose",
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
        "/linalg/eigenvalues",
        json={
            "matrix": [[2, 0], [0, 3]]
        },
    )

    assert response.status_code == 200
    assert sorted(response.json()["eigenvalues"]) == [2.0, 3.0]


def test_eigenvectors_endpoint_success_shape():

    response = client.post(
        "/linalg/eigenvectors",
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
        "/linalg/trace",
        json={
            "matrix": [[1, 2], [3, 4]]
        },
    )

    assert response.status_code == 200
    assert response.json()["trace"] == 5.0


def test_matrix_validation_ragged_returns_422():

    response = client.post(
        "/linalg/determinant",
        json={
            "matrix": [[1, 2], [3]]
        },
    )

    assert response.status_code == 422


def test_stats_summary_endpoint_success():

    response = client.post(
        "/stats/summary",
        json={
            "vector": [1, 2, 3, 4]
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["mean"] == pytest.approx(2.5)
    assert payload["std"] == pytest.approx(float(np.std([1, 2, 3, 4])))
    assert payload["minimum"] == 1.0
    assert payload["maximum"] == 4.0


def test_stats_mean_endpoint_success():

    response = client.post(
        "/stats/mean",
        json={
            "vector": [10, 20, 30]
        },
    )

    assert response.status_code == 200
    assert response.json()["mean"] == pytest.approx(20.0)


def test_stats_std_endpoint_success():

    data = [1, 2, 3, 4, 5]
    response = client.post(
        "/stats/std",
        json={
            "vector": data
        },
    )

    assert response.status_code == 200
    assert response.json()["std"] == pytest.approx(float(np.std(data)))


def test_stats_variance_endpoint_success():

    data = [1, 2, 3, 4, 5]
    response = client.post(
        "/stats/variance",
        json={
            "vector": data
        },
    )

    assert response.status_code == 200
    assert response.json()["variance"] == pytest.approx(float(np.var(data)))


def test_stats_max_endpoint_success():

    response = client.post(
        "/stats/max",
        json={
            "vector": [3, 9, 2, 7]
        },
    )

    assert response.status_code == 200
    assert response.json()["maximum"] == 9.0


def test_stats_min_endpoint_success():

    response = client.post(
        "/stats/min",
        json={
            "vector": [3, 9, 2, 7]
        },
    )

    assert response.status_code == 200
    assert response.json()["minimum"] == 2.0


def test_stats_empty_data_validation_returns_422():

    response = client.post(
        "/stats/mean",
        json={
            "vector": []
        },
    )

    assert response.status_code == 422


def test_matrix_addition_endpoint_success():

    response = client.post(
        "/linalg/matrix-addition",
        json={
            "matrix_a": [[1, 2], [3, 4]],
            "matrix_b": [[5, 6], [7, 8]],
        },
    )

    assert response.status_code == 200
    assert response.json()["result"] == [[6.0, 8.0], [10.0, 12.0]]


def test_matrix_addition_shape_mismatch_returns_422():

    response = client.post(
        "/linalg/matrix-addition",
        json={
            "matrix_a": [[1, 2], [3, 4]],
            "matrix_b": [[5, 6, 7], [8, 9, 10]],
        },
    )

    assert response.status_code == 422


def test_matrix_multiplication_incompatible_shapes_returns_422():

    response = client.post(
        "/linalg/matrix-multiplication",
        json={
            "matrix_a": [[1, 2, 3]],
            "matrix_b": [[4, 5, 6]],
        },
    )

    assert response.status_code == 422
    details = response.json().get("detail", [])
    messages = [item.get("msg", "") for item in details if isinstance(item, dict)]
    assert any(
        "columns in matrix a" in msg.lower() and "rows in matrix b" in msg.lower()
        for msg in messages
    )


def test_scalar_multiply_endpoint_success():

    response = client.post(
        "/linalg/scalar-multiply",
        json={
            "matrix": [[1, 2], [3, 4]],
            "scalar": 2,
        },
    )

    assert response.status_code == 200
    assert response.json()["result"] == [[2.0, 4.0], [6.0, 8.0]]


def test_scalar_divide_endpoint_success():

    response = client.post(
        "/linalg/scalar-divide",
        json={
            "matrix": [[2, 4], [6, 8]],
            "scalar": 2,
        },
    )

    assert response.status_code == 200
    assert response.json()["result"] == [[1.0, 2.0], [3.0, 4.0]]


def test_scalar_divide_by_zero_returns_400():

    response = client.post(
        "/linalg/scalar-divide",
        json={
            "matrix": [[1, 2], [3, 4]],
            "scalar": 0,
        },
    )

    assert response.status_code == 400
    assert "divide by zero" in response.json()["detail"].lower()


def test_register_rejects_password_longer_than_bcrypt_limit():
    response = client.post(
        "/auth/register",
        json={
            "username": f"user-{uuid4()}",
            "email": f"{uuid4()}@example.com",
            "password": "a" * 73,
        },
    )

    assert response.status_code == 422
    assert "72 bytes" in str(response.json()["detail"])


def test_login_rejects_password_longer_than_bcrypt_limit():
    response = client.post(
        "/auth/login",
        json={
            "username": "missing",
            "password": "a" * 73,
        },
    )

    assert response.status_code == 422
    assert "72 bytes" in str(response.json()["detail"])


def test_register_does_not_return_password_hash():
    username = f"user-{uuid4()}"
    response = client.post(
        "/auth/register",
        json={
            "username": username,
            "email": f"{uuid4()}@example.com",
            "password": "valid-password",
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["username"] == username
    assert "password_hash" not in payload
