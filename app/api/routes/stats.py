from fastapi import APIRouter, HTTPException
import logging

from app.api.models import schemas

from app.engine import stats

from app.engine.utils import exceptions

from app.types import Vector

router = APIRouter()

logger = logging.getLogger(__name__)

@router.post("/stats/summary", response_model=schemas.SummaryStatsResponse,
             summary="Compute summary statistics for a dataset",
             description="Returns summary statistics for the input dataset, including mean, standard deviation, minimum, and maximum values.")
def compute_summary(req: schemas.StatsRequest):
    logger.info("Computing Summary Statistics")
    
    try:
        result = stats.summary(req.data)
        
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )

    return result
@router.post("/mean", response_model=schemas.MeanResponse,
             summary="Compute the mean of a dataset",
             description="Returns the mean of the input dataset. The mean is the average value of the dataset.")
def compute_mean(req: schemas.StatsRequest):
    logger.info("Computing Mean")
    
    try:
        result = stats.mean(req.data)
        
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )

    return {
        "mean": result
    }
    
    
@router.post("/std", response_model=schemas.StdResponse,
             summary="Compute the standard deviation of a dataset",
             description="Returns the standard deviation of the input dataset. The standard deviation is a measure of the amount of variation or dispersion in a set of values.")
def compute_standard_deviation(req: schemas.StatsRequest):
    logger.info("Computing Standard Deviation")
    
    try:
        result = stats.std(req.data)
        
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )
        
    return {
        "std": result
    }
    
    
@router.post("/max", response_model=schemas.MaximumResponse,
             summary="Compute the maximum value of a dataset",
             description="Returns the maximum value of the input dataset. The maximum is the largest value in the dataset.")
def compute_maximum(req: schemas.StatsRequest):
    logger.info("Computing Maximum")
    
    try:
        result = stats.maximum(req.data)
        
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )
        
    return {
        "maximum": result
    }
    
    
@router.post("/min", response_model=schemas.MinimumResponse,
             summary="Compute the minimum value of a dataset",
             description="Returns the minimum value of the input dataset. The minimum is the smallest value in the dataset.")
def compute_minimum(req: schemas.StatsRequest):
    logger.info("Computing Minimum")
    
    try:
        result = stats.minimum(req.data)
        
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )
        
    return {
        "minimum": result
    }