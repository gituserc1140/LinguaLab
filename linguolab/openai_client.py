"""Optional OpenAI/Azure OpenAI integration for AI workbench."""

from __future__ import annotations

from typing import Any

from openai import AzureOpenAI, OpenAI

from linguolab.config import settings


def available() -> bool:
    return bool(settings.openai_api_key) or bool(
        settings.azure_openai_endpoint and settings.azure_openai_api_key and settings.azure_openai_deployment
    )


def completion(prompt: str) -> str:
    if settings.azure_openai_endpoint and settings.azure_openai_api_key and settings.azure_openai_deployment:
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

    if settings.openai_api_key:
        client = OpenAI(api_key=settings.openai_api_key)
        response = client.chat.completions.create(
            model=settings.openai_model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
        )
        return _content(response)

    raise RuntimeError("No OpenAI or Azure OpenAI credentials configured.")


def _content(response: Any) -> str:
    return response.choices[0].message.content or ""
