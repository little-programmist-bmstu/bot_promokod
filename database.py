import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "promo_bot.db"


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def get_promo_code_by_key(user_key: str) -> str | None:

    conn = get_connection()
    cursor = conn.cursor()

    query = f"SELECT promo_code FROM promo_codes WHERE key = '{user_key}'"
    print(f"[DEBUG] Выполняемый SQL: {query}")

    cursor.execute(query)
    row = cursor.fetchone()
    conn.close()

    if row is None:
        return None
    return row["promo_code"]


def mark_promo_as_used(promo_code: str) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE promo_codes SET is_used = 1 WHERE promo_code = ?",
        (promo_code,)
    )
    affected = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return affected
