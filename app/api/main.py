from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import inspect, text

from app.db.database import Base, engine
from app.api.routes import auth, linalg, stats, ode, notes
import app.logging_config

Base.metadata.create_all(bind=engine)


def ensure_sqlite_note_owner_column():
    if not engine.url.drivername.startswith("sqlite"):
        return

    inspector = inspect(engine)
    columns = {
        column["name"]
        for column in inspector.get_columns("notes")
    }

    if "user_id" in columns:
        return

    with engine.begin() as connection:
        connection.execute(
            text("ALTER TABLE notes ADD COLUMN user_id INTEGER")
        )


ensure_sqlite_note_owner_column()

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

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "http://127.0.0.1:8000",
        "http://localhost:8000",
        "null",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
    
