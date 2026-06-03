from . import linalg
from . import ode
from . import stats
from .linalg import router
from .stats import router
from .ode import router

__all__ = [
    "linalg",
    "ode",
    "stats",
    "router",
]
