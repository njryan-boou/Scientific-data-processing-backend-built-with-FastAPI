from fastapi import APIRouter, HTTPException
import logging

from app.api.models import schemas

from app.engine import ode

from app.engine.utils import exceptions

from app.types import Matrix, Vector

router = APIRouter()

logger = logging.getLogger(__name__)


@router.post("/euler", response_model=schemas.EulerResponse,
             summary="Compute the solution of an ODE using the Euler method",
             description="Returns the solution of the input ordinary differential equation (ODE) using the Euler method. The Euler method is a simple numerical technique for solving ODEs.")
def compute_euler(req: schemas.EulerRequest) -> dict[str, Vector]:
    logger.info("Computing Euler method solution")
    
    try:
        t, y = ode.euler_method(
            y0=req.y0,
            t0=req.t0,
            step_size=req.step_size,
            steps=req.steps
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
        
    return {
        "t": t,
        "y": y
    }