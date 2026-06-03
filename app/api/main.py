from fastapi import FastAPI

from app.api.routes import linalg, stats, ode
from app import logging_config


app = FastAPI()


app.include_router(linalg.router)
app.include_router(stats.router)
app.include_router(ode.router)


@app.get("/health")
def health():

    return {
        "status": "running"
    }