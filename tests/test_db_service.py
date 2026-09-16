from linguolab.services import LinguaLabService


def test_history_persistence(tmp_path):
    db_path = tmp_path / "test.db"
    svc = LinguaLabService(db_path=str(db_path))

    svc.writing_analytics("This sentence is clear.")
    history = svc.history(limit=5)

    assert len(history) == 1
    assert history[0]["module"] == "writing_analytics"
