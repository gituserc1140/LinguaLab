"""Runtime configuration for LinguaLab."""

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    app_name: str = "LinguaLab"
    sqlite_path: str = os.getenv("LINGUALAB_DB_PATH", "lingualab.db")
    openai_api_key: str | None = os.getenv("OPENAI_API_KEY")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    azure_openai_endpoint: str | None = os.getenv("AZURE_OPENAI_ENDPOINT")
    azure_openai_api_key: str | None = os.getenv("AZURE_OPENAI_API_KEY")
    azure_openai_api_version: str = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-01")
    azure_openai_deployment: str | None = os.getenv("AZURE_OPENAI_DEPLOYMENT")


settings = Settings()
