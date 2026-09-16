"""SQLite persistence for analysis history."""

from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCHEMA = """
CREATE TABLE IF NOT EXISTS analysis_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    module TEXT NOT NULL,
    input_preview TEXT NOT NULL,
    output_json TEXT NOT NULL,
    created_at TEXT NOT NULL
);
"""


def get_connection(path: str) -> sqlite3.Connection:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    conn.execute(SCHEMA)
    conn.commit()
    return conn


def save_analysis(path: str, module: str, input_text: str, output_data: dict[str, Any]) -> None:
    conn = get_connection(path)
    preview = " ".join(input_text.split())[:240]
    conn.execute(
        "INSERT INTO analysis_history (module, input_preview, output_json, created_at) VALUES (?, ?, ?, ?)",
        (module, preview, json.dumps(output_data), datetime.now(timezone.utc).isoformat()),
    )
    conn.commit()
    conn.close()


def recent_analyses(path: str, limit: int = 10) -> list[dict[str, Any]]:
    conn = get_connection(path)
    rows = conn.execute(
        "SELECT module, input_preview, output_json, created_at FROM analysis_history ORDER BY id DESC LIMIT ?",
        (limit,),
    ).fetchall()
    conn.close()
    return [
        {
            "module": row[0],
            "input_preview": row[1],
            "output": json.loads(row[2]),
            "created_at": row[3],
        }
        for row in rows
    ]
