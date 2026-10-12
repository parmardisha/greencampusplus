import sqlite3
from datetime import datetime, timezone
from pathlib import Path

DATABASE_PATH = Path(__file__).with_name("greenpulse.db")


def _connect():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    with _connect() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS activities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                description TEXT NOT NULL,
                category TEXT NOT NULL,
                amount REAL NOT NULL CHECK (amount > 0),
                emissions_kg REAL NOT NULL CHECK (emissions_kg >= 0),
                created_at TEXT NOT NULL
            )
            """
        )


def _activity_dict(row):
    return {
        "id": row["id"],
        "description": row["description"],
        "category": row["category"],
        "amount": row["amount"],
        "emissions_kg": row["emissions_kg"],
        "created_at": row["created_at"],
    }


def add_activity(description, category, amount, emissions_kg):
    created_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    with _connect() as connection:
        cursor = connection.execute(
            """
            INSERT INTO activities (description, category, amount, emissions_kg, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (description, category, amount, emissions_kg, created_at),
        )
        row = connection.execute(
            "SELECT * FROM activities WHERE id = ?", (cursor.lastrowid,)
        ).fetchone()
    return _activity_dict(row)


def get_activities(limit=50):
    with _connect() as connection:
        rows = connection.execute(
            "SELECT * FROM activities ORDER BY created_at DESC, id DESC LIMIT ?",
            (limit,),
        ).fetchall()
    return [_activity_dict(row) for row in rows]


def get_summary():
    with _connect() as connection:
        row = connection.execute(
            """
            SELECT COUNT(*) AS activity_count,
                   COALESCE(SUM(emissions_kg), 0) AS total_kg,
                   COALESCE(AVG(emissions_kg), 0) AS average_kg
            FROM activities
            """
        ).fetchone()
    return {
        "activity_count": row["activity_count"],
        "total_kg": round(row["total_kg"], 2),
        "average_kg": round(row["average_kg"], 2),
    }


def delete_activity(activity_id):
    with _connect() as connection:
        cursor = connection.execute(
            "DELETE FROM activities WHERE id = ?", (activity_id,)
        )
    return cursor.rowcount > 0
