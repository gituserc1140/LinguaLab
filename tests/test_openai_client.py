import types

import linguolab.openai_client as oc
import pytest


class _Resp:
    def __init__(self, text):
        self.choices = [types.SimpleNamespace(message=types.SimpleNamespace(content=text))]


class _ChatCompletions:
    def __init__(self, text):
        self._text = text

    def create(self, **kwargs):
        return _Resp(self._text)


class _Client:
    def __init__(self, text):
        self.chat = types.SimpleNamespace(completions=_ChatCompletions(text))


def test_available_flags(monkeypatch):
    monkeypatch.setattr(oc.settings, "ai_provider", "auto")
    monkeypatch.setattr(oc.settings, "openai_api_key", None)
    monkeypatch.setattr(oc.settings, "azure_openai_endpoint", None)
    monkeypatch.setattr(oc.settings, "azure_openai_api_key", None)
    monkeypatch.setattr(oc.settings, "azure_openai_deployment", None)
    assert oc.available() is False

    monkeypatch.setattr(oc.settings, "openai_api_key", "k")
    assert oc.available() is True


def test_completion_uses_openai(monkeypatch):
    fake_module = types.SimpleNamespace(OpenAI=lambda api_key: _Client("ok"), AzureOpenAI=lambda **kwargs: _Client("azure"))
    monkeypatch.setattr(oc.settings, "ai_provider", "openai")
    monkeypatch.setattr(oc.settings, "openai_api_key", "k")
    monkeypatch.setattr(oc.settings, "azure_openai_endpoint", None)
    monkeypatch.setitem(__import__("sys").modules, "openai", fake_module)

    assert oc.completion("hi") == "ok"


def test_completion_uses_azure(monkeypatch):
    captured = {}

    def _azure(**kwargs):
        captured.update(kwargs)
        return _Client("azure")

    fake_module = types.SimpleNamespace(OpenAI=lambda api_key: _Client("ok"), AzureOpenAI=_azure)
    monkeypatch.setitem(__import__("sys").modules, "openai", fake_module)
    monkeypatch.setattr(oc.settings, "ai_provider", "azure")
    monkeypatch.setattr(oc.settings, "openai_api_key", None)
    monkeypatch.setattr(oc.settings, "azure_openai_endpoint", "https://example.azure.com")
    monkeypatch.setattr(oc.settings, "azure_openai_api_key", "k")
    monkeypatch.setattr(oc.settings, "azure_openai_api_version", "2024-02-01")
    monkeypatch.setattr(oc.settings, "azure_openai_deployment", "dep")

    assert oc.completion("hi") == "azure"
    assert captured["api_version"] == "2024-02-01"


def test_invalid_provider_raises_value_error():
    with pytest.raises(ValueError):
        oc.available(provider="invalid-provider")


def test_resolve_runtime_provider_prefers_configured_backend(monkeypatch):
    monkeypatch.setattr(oc.settings, "ai_provider", "auto")
    monkeypatch.setattr(oc.settings, "openai_api_key", "k")
    monkeypatch.setattr(oc.settings, "azure_openai_endpoint", "https://example.azure.com")
    monkeypatch.setattr(oc.settings, "azure_openai_api_key", "k")
    monkeypatch.setattr(oc.settings, "azure_openai_deployment", "dep")
    assert oc.resolve_runtime_provider("auto") == "azure"


def test_resolve_runtime_provider_uses_openai_when_only_openai_configured(monkeypatch):
    monkeypatch.setattr(oc.settings, "ai_provider", "auto")
    monkeypatch.setattr(oc.settings, "openai_api_key", "k")
    monkeypatch.setattr(oc.settings, "azure_openai_endpoint", None)
    monkeypatch.setattr(oc.settings, "azure_openai_api_key", None)
    monkeypatch.setattr(oc.settings, "azure_openai_deployment", None)
    assert oc.resolve_runtime_provider("auto") == "openai"


def test_resolve_runtime_provider_returns_auto_when_unconfigured(monkeypatch):
    monkeypatch.setattr(oc.settings, "ai_provider", "auto")
    monkeypatch.setattr(oc.settings, "openai_api_key", None)
    monkeypatch.setattr(oc.settings, "azure_openai_endpoint", None)
    monkeypatch.setattr(oc.settings, "azure_openai_api_key", None)
    monkeypatch.setattr(oc.settings, "azure_openai_deployment", None)
    assert oc.resolve_runtime_provider("auto") == "auto"
