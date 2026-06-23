from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import inspect, text

from app.config import settings
from app.db.database import Base, engine
from app.api.routes import admin, auth, linalg, stats, ode, notes
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


def ensure_sqlite_user_admin_column():
    if not engine.url.drivername.startswith("sqlite"):
        return

    inspector = inspect(engine)
    columns = {
        column["name"]
        for column in inspector.get_columns("users")
    }

    if "is_admin" in columns:
        return

    with engine.begin() as connection:
        connection.execute(
            text("ALTER TABLE users ADD COLUMN is_admin BOOLEAN NOT NULL DEFAULT 0")
        )


ensure_sqlite_note_owner_column()
ensure_sqlite_user_admin_column()

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

Built with FastAPI and C++.
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
        "https://scientific-data-processing-backend.vercel.app/"
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
app.include_router(admin.router, prefix="/admin", tags=["Admin"])

@app.get("/health")
def health():

    return {
        "status": "running"
    }