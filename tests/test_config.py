import os

import pytest

from app.config import Settings, load_env_file


def test_load_env_file_sets_missing_values_without_overriding_existing(tmp_path, monkeypatch):
    env_file = tmp_path / ".env"
    env_file.write_text(
        "\n".join([
            "JWT_SECRET_KEY=from-file",
            "DATABASE_URL='sqlite:///from-file.db'",
            "IGNORED_LINE",
            "# comment",
        ]),
        encoding="utf-8",
    )

    monkeypatch.setenv("JWT_SECRET_KEY", "already-set")
    monkeypatch.delenv("DATABASE_URL", raising=False)
    monkeypatch.delenv("IGNORED_LINE", raising=False)

    load_env_file(env_file)

    assert os.environ["JWT_SECRET_KEY"] == "already-set"
    assert os.environ["DATABASE_URL"] == "sqlite:///from-file.db"
    assert "IGNORED_LINE" not in os.environ


def test_settings_generates_development_secret_when_missing(monkeypatch):
    monkeypatch.setenv("APP_ENV", "development")
    monkeypatch.delenv("JWT_SECRET_KEY", raising=False)

    settings = Settings()

    assert settings.jwt_secret_key


def test_settings_requires_jwt_secret_in_production(monkeypatch):
    monkeypatch.setenv("APP_ENV", "production")
    monkeypatch.delenv("JWT_SECRET_KEY", raising=False)

    with pytest.raises(RuntimeError, match="JWT_SECRET_KEY"):
        Settings()


def test_settings_parses_cors_origins(monkeypatch):
    monkeypatch.setenv(
        "CORS_ORIGINS",
        "http://localhost:5500, http://127.0.0.1:5500",
    )

    settings = Settings()

    assert settings.cors_origins == (
        "http://localhost:5500",
        "http://127.0.0.1:5500",
    )
