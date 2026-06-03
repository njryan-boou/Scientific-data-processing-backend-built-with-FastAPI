import numpy as np
from app.engine.utils import validation
from app.types import Vector, Matrix


def euler_method (y0: float, t0: float, step_size: float, steps: int) -> tuple[Vector, Vector]:
    t = np.array([t0 + i * step_size for i in range(steps)], dtype=np.float64)
    y = y0 * np.exp(t - t0)
    return t.tolist(), y.tolist()