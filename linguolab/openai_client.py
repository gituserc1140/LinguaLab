"""Optional OpenAI/Azure OpenAI integration for AI workbench."""

from __future__ import annotations

from typing import Any

from linguolab.config import settings


def _azure_configured() -> bool:
    return bool(
        settings.azure_openai_endpoint and settings.azure_openai_api_key and settings.azure_openai_deployment
    )


def _openai_configured() -> bool:
    return bool(settings.openai_api_key)


def available(provider: str = "auto") -> bool:
    selected = _resolve_provider(provider)
    if selected == "azure":
        return _azure_configured()
    if selected == "openai":
        return _openai_configured()
    return _openai_configured() or _azure_configured()


def completion(prompt: str, provider: str = "auto") -> str:
    selected = resolve_runtime_provider(provider)

    if selected == "azure" and _azure_configured():
        from openai import AzureOpenAI

        client = AzureOpenAI(
            api_key=settings.azure_openai_api_key,
            api_version=settings.azure_openai_api_version,
            azure_endpoint=settings.azure_openai_endpoint,
        )
        response = client.chat.completions.create(
            model=settings.azure_openai_deployment,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
        )
        return _content(response)

    if selected == "openai" and _openai_configured():
        from openai import OpenAI

        client = OpenAI(api_key=settings.openai_api_key)
        response = client.chat.completions.create(
            model=settings.openai_model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
        )
        return _content(response)

    raise RuntimeError("No OpenAI or Azure OpenAI credentials configured.")


def _resolve_provider(provider: str) -> str:
    selected = (provider or "auto").lower()
    if selected == "auto":
        selected = (settings.ai_provider or "auto").lower()
    if selected not in {"auto", "openai", "azure"}:
        raise ValueError("provider must be one of: auto, openai, azure")
    return selected


def resolve_runtime_provider(provider: str = "auto") -> str:
    selected = _resolve_provider(provider)
    if selected in {"openai", "azure"}:
        return selected
    if _azure_configured():
        return "azure"
    if _openai_configured():
        return "openai"
    return "auto"


def _content(response: Any) -> str:
    return response.choices[0].message.content or ""
