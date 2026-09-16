from linguolab.services import LinguaLabService
from linguolab import openai_client


def test_ai_workbench_falls_back_when_openai_import_fails(monkeypatch, tmp_path):
    svc = LinguaLabService(db_path=str(tmp_path / "svc.db"))

    monkeypatch.setattr(openai_client, "available", lambda provider="auto": True)

    def _raise(*args, **kwargs):
        raise ModuleNotFoundError("openai not installed")

    monkeypatch.setattr(openai_client, "completion", _raise)

    result = svc.ai_language_workbench("This is a demo text for summarisation.")

    assert result["provider"] == "local-demo"
    assert "provider_error" in result
