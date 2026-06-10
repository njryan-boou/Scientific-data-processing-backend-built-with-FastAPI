from fastapi import APIRouter, HTTPException
import logging

import app.api.models as schemas

from app.engine import ode

from app.types import Vector

router = APIRouter()

logger = logging.getLogger(__name__)


@router.post("/euler", response_model=schemas.EulerResponse,
             summary="Compute the solution of an ODE using the Euler method",
             description="""
Computes the solution of an ordinary differential equation (ODE) using the Euler method.

Requirements:
- Initial value (y0) must be provided.
- Initial time (t0) must be provided.
- Step size must be provided and positive.
- Number of steps must be provided and positive.

Returns the time points and corresponding solution values of the ODE.
"""
)
def compute_euler(req: schemas.EulerRequest) -> dict[str, Vector]:
    logger.info("Computing Euler method solution")
    
    try:
        t, y = ode.euler_method(
            y0=req.y0,
            t0=req.t0,
            step_size=req.step_size,
            steps=req.steps
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except Exception:
        logger.exception("Unexpected error while computing Euler solution")
        raise HTTPException(status_code=500, detail="Internal server error")
        
    return {
        "t": t,
        "y": y
    }
    
    
@router.post("/runge-kutta-4", response_model=schemas.RungeKuttaResponse,
             summary="Compute the solution of an ODE using the Runge-Kutta 4 method",
             description="""
Computes the solution of an ordinary differential equation (ODE) using the Runge-Kutta 4 method.

Requirements:
- Initial value (y0) must be provided.
- Initial time (t0) must be provided.
- Step size must be provided and positive.
- Number of steps must be provided and positive.

Returns the time points and corresponding solution values of the ODE.
"""
)
def compute_runge_kutta_4(req: schemas.EulerRequest) -> dict[str, Vector]:
    logger.info("Computing Runge-Kutta 4 method solution")
    
    try:
        t, y = ode.runge_kutta_4(
            y0=req.y0,
            t0=req.t0,
            step_size=req.step_size,
            steps=req.steps
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except Exception:
        logger.exception("Unexpected error while computing Runge-Kutta 4 solution")
        raise HTTPException(status_code=500, detail="Internal server error")
        
    return {
        "t": t,
        "y": y
    }