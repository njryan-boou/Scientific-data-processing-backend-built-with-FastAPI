from fastapi import FastAPI

from app.db.database import Base, engine
from app.api.routes import auth, linalg, stats, ode, notes
import app.logging_config

Base.metadata.create_all(bind=engine)

tags_metadata = [
    {
        "name": "Linear Algebra",
        "description": "Matrix operations and decompositions."
    },
    {
        "name": "Statistics",
        "description": "Descriptive statistics and data analysis."
    },
    {
        "name": "Ordinary Differential Equations",
        "description": "Numerical methods for solving ODEs."
    }
]

app = FastAPI(
    title="Scientific Math API",
    version="1.0.0",
    description="""
Scientific Computing API

Features:
- Linear Algebra
- Statistics
- Differential Equations

Built with FastAPI and NumPy.
""",

    openapi_tags=tags_metadata,
    contact={
        "name": "Noah Ryan",
        "url": "https://github.com/njryan-boou"
    }
)


app.include_router(linalg.router, prefix="/linalg", tags=["Linear Algebra"])
app.include_router(stats.router, prefix="/stats", tags=["Statistics"])
app.include_router(ode.router, prefix="/ode", tags=["Ordinary Differential Equations"])
app.include_router(notes.router, prefix="/notes", tags=["Notes"])
app.include_router(auth.router, prefix="/auth", tags=["Auth"])

@app.get("/health")
def health():

    return {
        "status": "running"
    }
    
