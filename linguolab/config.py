"""Runtime configuration for LinguaLab."""

import os
from dataclasses import dataclass, field


@dataclass
class Settings:
    app_name: str = "LinguaLab"
    ai_provider: str = field(default_factory=lambda: os.getenv("LINGUALAB_AI_PROVIDER", "auto"))
    sqlite_path: str = field(default_factory=lambda: os.getenv("LINGUALAB_DB_PATH", "lingualab.db"))
    openai_api_key: str | None = field(default_factory=lambda: os.getenv("OPENAI_API_KEY"))
    openai_model: str = field(default_factory=lambda: os.getenv("OPENAI_MODEL", "gpt-4o-mini"))
    azure_openai_endpoint: str | None = field(default_factory=lambda: os.getenv("AZURE_OPENAI_ENDPOINT"))
    azure_openai_api_key: str | None = field(default_factory=lambda: os.getenv("AZURE_OPENAI_API_KEY"))
    azure_openai_api_version: str = field(default_factory=lambda: os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-01"))
    azure_openai_deployment: str | None = field(default_factory=lambda: os.getenv("AZURE_OPENAI_DEPLOYMENT"))


settings = Settings()
