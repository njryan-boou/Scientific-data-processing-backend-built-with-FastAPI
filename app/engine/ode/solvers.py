import numpy as np
from app.types import Vector


def euler_method(y0: float, t0: float, step_size: float, steps: int) -> tuple[Vector, Vector]:
    t = np.array([t0 + i * step_size for i in range(steps)], dtype=np.float64)
    y = y0 * np.exp(t - t0)
    return t.tolist(), y.tolist()


def runge_kutta_4(y0: float, t0: float, step_size: float, steps: int) -> tuple[Vector, Vector]:
    t = np.array([t0 + i * step_size for i in range(steps)], dtype=np.float64)
    y = np.zeros(steps, dtype=np.float64)
    y[0] = y0

    for i in range(1, steps):
        k1 = y[i-1]
        k2 = y[i-1] + 0.5 * step_size * k1
        k3 = y[i-1] + 0.5 * step_size * k2
        k4 = y[i-1] + step_size * k3
        y[i] = y[i-1] + (step_size / 6) * (k1 + 2*k2 + 2*k3 + k4)

    return t.tolist(), y.tolist()