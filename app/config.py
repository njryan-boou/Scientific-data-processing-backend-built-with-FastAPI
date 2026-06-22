import os
import secrets
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
ENV_FILE = PROJECT_ROOT / ".env"


def load_env_file(path: Path = ENV_FILE) -> None:
    if not path.exists():
        return

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()

        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")

        if key:
            os.environ.setdefault(key, value)


def _csv_env(name: str, default: str) -> tuple[str, ...]:
    value = os.getenv(name, default)
    return tuple(
        item.strip()
        for item in value.split(",")
        if item.strip()
    )


def _int_env(name: str, default: int) -> int:
    value = os.getenv(name)

    if value is None:
        return default

    return int(value)


load_env_file()


class Settings:
    def __init__(self):
        self.app_env = os.getenv("APP_ENV", "development")
        self.database_url = os.getenv("DATABASE_URL")
        self.jwt_algorithm = os.getenv("JWT_ALGORITHM", "HS256")
        self.access_token_expire_hours = _int_env(
            "ACCESS_TOKEN_EXPIRE_HOURS",
            24
        )
        self.cors_origins = _csv_env(
            "CORS_ORIGINS",
            "http://127.0.0.1:5500,http://localhost:5500,http://127.0.0.1:8001,http://localhost:8001,null",
        )

        self.jwt_secret_key = os.getenv("JWT_SECRET_KEY")

        if not self.jwt_secret_key:
            if self.app_env == "production":
                raise RuntimeError("JWT_SECRET_KEY must be set in production")

            self.jwt_secret_key = secrets.token_urlsafe(32)


settings = Settings()
