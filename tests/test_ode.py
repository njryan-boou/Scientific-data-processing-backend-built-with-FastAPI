import numpy as np
import pytest
from fastapi.testclient import TestClient

from app.api.main import app
from app.engine import ode


client = TestClient(app)


def test_euler_method_returns_expected_values():

	y0 = 2.0
	t0 = 0.0
	step_size = 0.5
	steps = 4

	t, y = ode.euler_method(y0=y0, t0=t0, step_size=step_size, steps=steps)

	expected_t = [0.0, 0.5, 1.0, 1.5]
	expected_y = (y0 * np.exp(np.array(expected_t) - t0)).tolist()

	assert t == expected_t
	assert np.allclose(y, expected_y)


def test_euler_method_single_step():

	t, y = ode.euler_method(y0=1.5, t0=2.0, step_size=0.25, steps=1)

	assert t == [2.0]
	assert y == pytest.approx([1.5])


def test_euler_endpoint_success():

	payload = {
		"y0": 1.0,
		"t0": 0.0,
		"step_size": 0.5,
		"steps": 3,
	}

	response = client.post("/ode/euler", json=payload)

	assert response.status_code == 200
	body = response.json()
	assert body["t"] == [0.0, 0.5, 1.0]
	assert body["y"] == pytest.approx((np.exp(np.array([0.0, 0.5, 1.0]))).tolist())


def test_euler_endpoint_non_positive_steps_returns_422():

	response = client.post(
		"/ode/euler",
		json={
			"y0": 1.0,
			"t0": 0.0,
			"step_size": 0.1,
			"steps": 0,
		},
	)

	assert response.status_code == 422


def test_euler_endpoint_non_positive_step_size_returns_422():

	response = client.post(
		"/ode/euler",
		json={
			"y0": 1.0,
			"t0": 0.0,
			"step_size": -0.1,
			"steps": 10,
		},
	)

	assert response.status_code == 422
