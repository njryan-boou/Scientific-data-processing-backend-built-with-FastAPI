from fastapi import APIRouter, HTTPException
import logging

import app.api.models as schemas

from app.engine import stats

router = APIRouter()

logger = logging.getLogger(__name__)

@router.post("/summary", response_model=schemas.SummaryStatsResponse,
             summary="Compute summary statistics for a dataset",
             description="""
Computes summary statistics for a dataset, including mean, standard deviation, minimum, and maximum values.

Requirements:
- Dataset must be provided.

Returns the summary statistics of the dataset.
"""
)
def compute_summary(req: schemas.VectorRequest) -> dict[str, float]:
    logger.info("Computing Summary Statistics")
    
    try:
        result = stats.summary(req.vector)
        
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )
    except Exception:
        logger.exception("Unexpected error while computing summary stats")
        raise HTTPException(status_code=500, detail="Internal server error")

    return result
@router.post("/mean", response_model=schemas.MeanResponse,
             summary="Compute the mean of a dataset",
             description="""
Computes the mean of a dataset.

Requirements:
- Dataset must be provided.

Returns the mean of the dataset.
"""
)
def compute_mean(req: schemas.VectorRequest) -> dict[str, float]:
    logger.info("Computing Mean")
    
    try:
        result = stats.mean(req.vector)
        
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )
    except Exception:
        logger.exception("Unexpected error while computing mean")
        raise HTTPException(status_code=500, detail="Internal server error")

    return {
        "mean": result
    }
    
    
@router.post("/std", response_model=schemas.StdResponse,
             summary="Compute the standard deviation of a dataset",
             description="""
Computes the standard deviation of a dataset.

Requirements:
- Dataset must be provided.

Returns the standard deviation of the dataset.
"""
)
def compute_standard_deviation(req: schemas.VectorRequest) -> dict[str, float]:
    logger.info("Computing Standard Deviation")
    
    try:
        result = stats.std(req.vector)
        
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )
    except Exception:
        logger.exception("Unexpected error while computing standard deviation")
        raise HTTPException(status_code=500, detail="Internal server error")
        
    return {
        "std": result
    }


@router.post("/variance", response_model=schemas.VarianceResponse,
             summary="Compute the variance of a dataset",
             description="""
Computes the variance of a dataset.

Requirements:
- Dataset must be provided.

Returns the variance of the dataset.
"""
)
def compute_variance(req: schemas.VectorRequest) -> dict[str, float]:
    logger.info("Computing Variance")

    try:
        result = stats.variance(req.vector)

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )
    except Exception:
        logger.exception("Unexpected error while computing variance")
        raise HTTPException(status_code=500, detail="Internal server error")

    return {
        "variance": result
    }
    
    
@router.post("/max", response_model=schemas.MaximumResponse,
             summary="Compute the maximum value of a dataset",
             description="""
Computes the maximum value of a dataset.

Requirements:
- Dataset must be provided.

Returns the maximum value of the dataset.
"""
)
def compute_maximum(req: schemas.VectorRequest) -> dict[str, float]:
    logger.info("Computing Maximum")
    
    try:
        result = stats.maximum(req.vector)
        
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )
    except Exception:
        logger.exception("Unexpected error while computing maximum")
        raise HTTPException(status_code=500, detail="Internal server error")
        
    return {
        "maximum": result
    }
    
    
@router.post("/min", response_model=schemas.MinimumResponse,
             summary="Compute the minimum value of a dataset",
             description="""
Computes the minimum value of a dataset.

Requirements:
- Dataset must be provided.

Returns the minimum value of the dataset.
"""
)
def compute_minimum(req: schemas.VectorRequest) -> dict[str, float]:
    logger.info("Computing Minimum")
    
    try:
        result = stats.minimum(req.vector)
        
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )
    except Exception:
        logger.exception("Unexpected error while computing minimum")
        raise HTTPException(status_code=500, detail="Internal server error")
        
    return {
        "minimum": result
    }
    
    
