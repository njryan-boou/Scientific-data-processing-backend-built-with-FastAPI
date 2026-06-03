import numpy as np
import pytest

from app.engine import stats


def test_mean_basic():

	data = [1, 2, 3, 4, 5]

	assert stats.mean(data) == pytest.approx(3.0)


def test_std_basic():

	data = [1, 2, 3, 4, 5]

	assert stats.std(data) == pytest.approx(float(np.std(data)))


def test_minimum_basic():

	data = [8, -2, 10, 1]

	assert stats.minimum(data) == -2.0


def test_maximum_basic():

	data = [8, -2, 10, 1]

	assert stats.maximum(data) == 10.0


def test_summary_basic():

	data = [1, 2, 3, 4]

	result = stats.summary(data)

	assert result["mean"] == pytest.approx(2.5)
	assert result["std"] == pytest.approx(float(np.std(data)))
	assert result["minimum"] == 1.0
	assert result["maximum"] == 4.0


def test_mean_empty_data_raises():

	with pytest.raises(ValueError):
		stats.mean([])


def test_summary_empty_data_raises():

	with pytest.raises(ValueError):
		stats.summary([])
