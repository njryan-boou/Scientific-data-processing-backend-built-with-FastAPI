from fastapi import FastAPI

from app.api.routes import linalg
from app import logging_config


app = FastAPI()


app.include_router(linalg.router)


@app.get("/health")
def health():

    return {
        "status": "running"
    }