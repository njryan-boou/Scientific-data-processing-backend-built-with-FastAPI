import os
from fastapi.testclient import TestClient
from jose import jwt
import numpy as np
import pytest
from uuid import uuid4

os.environ["DATABASE_URL"] = "sqlite:///./test_api.db"

from app.config import settings
from app.api.main import app
from app.api.services.security import create_access_token
from app.db import models
from app.db.database import SessionLocal


client = TestClient(app)


@pytest.fixture(autouse=True)
def clean_test_database():
    with SessionLocal() as db:
        db.query(models.Note).delete(synchronize_session=False)
        db.query(models.User).delete(synchronize_session=False)
        db.commit()


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


def test_access_token_uses_configured_jwt_settings():
    token = create_access_token({"sub": "configured-user"})

    payload = jwt.decode(
        token,
        settings.jwt_secret_key,
        algorithms=[settings.jwt_algorithm],
    )

    assert payload["sub"] == "configured-user"
    assert "exp" in payload


def register_and_login_user(admin=False):
    username = f"user-{uuid4()}"
    password = "valid-password"

    register_response = client.post(
        "/auth/register",
        json={
            "username": username,
            "email": f"{uuid4()}@example.com",
            "password": password,
        },
    )
    assert register_response.status_code == 200
    user_id = register_response.json()["id"]

    with SessionLocal() as db:
        user = (
            db.query(models.User)
            .filter(models.User.id == user_id)
            .first()
        )
        user.is_admin = admin
        db.commit()

    login_response = client.post(
        "/auth/login",
        json={
            "username": username,
            "password": password,
        },
    )
    assert login_response.status_code == 200

    token = login_response.json()["access_token"]
    return user_id, {
        "Authorization": f"Bearer {token}"
    }


def test_notes_require_authentication():
    response = client.get("/notes/")

    assert response.status_code == 401


def test_notes_are_scoped_to_current_user():
    _, first_user_headers = register_and_login_user()
    _, second_user_headers = register_and_login_user()

    first_note_response = client.post(
        "/notes/",
        headers=first_user_headers,
        json={
            "title": "First user's note",
            "content": "Visible only to the first user",
        },
    )
    assert first_note_response.status_code == 200
    first_note_id = first_note_response.json()["id"]

    second_note_response = client.post(
        "/notes/",
        headers=second_user_headers,
        json={
            "title": "Second user's note",
            "content": "Visible only to the second user",
        },
    )
    assert second_note_response.status_code == 200

    first_user_notes = client.get(
        "/notes/",
        headers=first_user_headers,
    )
    assert first_user_notes.status_code == 200
    first_user_titles = {
        note["title"]
        for note in first_user_notes.json()
    }
    assert "First user's note" in first_user_titles
    assert "Second user's note" not in first_user_titles

    second_user_notes = client.get(
        "/notes/",
        headers=second_user_headers,
    )
    assert second_user_notes.status_code == 200
    second_user_titles = {
        note["title"]
        for note in second_user_notes.json()
    }
    assert "Second user's note" in second_user_titles
    assert "First user's note" not in second_user_titles

    forbidden_delete = client.delete(
        f"/notes/{first_note_id}",
        headers=second_user_headers,
    )
    assert forbidden_delete.status_code == 404


def test_user_cannot_read_or_update_another_users_note():
    _, owner_headers = register_and_login_user()
    _, other_user_headers = register_and_login_user()

    create_response = client.post(
        "/notes/",
        headers=owner_headers,
        json={
            "title": "Private note",
            "content": "Only the owner can read or update this",
        },
    )
    assert create_response.status_code == 200
    note_id = create_response.json()["id"]

    read_response = client.get(
        f"/notes/{note_id}",
        headers=other_user_headers,
    )
    assert read_response.status_code == 404

    update_response = client.put(
        f"/notes/{note_id}",
        headers=other_user_headers,
        json={
            "title": "Changed by another user",
        },
    )
    assert update_response.status_code == 404

    owner_read_response = client.get(
        f"/notes/{note_id}",
        headers=owner_headers,
    )
    assert owner_read_response.status_code == 200
    assert owner_read_response.json()["title"] == "Private note"


def test_non_admin_cannot_access_admin_users():
    _, headers = register_and_login_user()

    response = client.get(
        "/admin/users",
        headers=headers,
    )

    assert response.status_code == 403


def test_admin_can_list_and_update_users():
    _, admin_headers = register_and_login_user(admin=True)
    user_id, user_headers = register_and_login_user()

    note_response = client.post(
        "/notes/",
        headers=user_headers,
        json={
            "title": "Managed user's note",
            "content": "Counted in the admin panel",
        },
    )
    assert note_response.status_code == 200

    list_response = client.get(
        "/admin/users",
        headers=admin_headers,
    )
    assert list_response.status_code == 200

    managed_user = next(
        user
        for user in list_response.json()
        if user["id"] == user_id
    )
    assert managed_user["note_count"] == 1
    assert managed_user["is_admin"] is False

    update_response = client.put(
        f"/admin/users/{user_id}",
        headers=admin_headers,
        json={
            "username": f"managed-{uuid4()}",
            "email": f"{uuid4()}@example.com",
            "is_admin": True,
        },
    )
    assert update_response.status_code == 200
    assert update_response.json()["is_admin"] is True


def test_admin_can_delete_user_and_notes():
    _, admin_headers = register_and_login_user(admin=True)
    user_id, user_headers = register_and_login_user()

    note_response = client.post(
        "/notes/",
        headers=user_headers,
        json={
            "title": "Deleted with user",
            "content": "This note should be deleted too",
        },
    )
    assert note_response.status_code == 200
    note_id = note_response.json()["id"]

    delete_response = client.delete(
        f"/admin/users/{user_id}",
        headers=admin_headers,
    )
    assert delete_response.status_code == 200

    with SessionLocal() as db:
        assert db.get(models.User, user_id) is None
        assert db.get(models.Note, note_id) is None


def test_admin_cannot_delete_or_demote_self():
    admin_id, admin_headers = register_and_login_user(admin=True)

    demote_response = client.put(
        f"/admin/users/{admin_id}",
        headers=admin_headers,
        json={
            "is_admin": False,
        },
    )
    assert demote_response.status_code == 400

    delete_response = client.delete(
        f"/admin/users/{admin_id}",
        headers=admin_headers,
    )
    assert delete_response.status_code == 400
