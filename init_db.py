import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "promo_bot.db"


TEST_DATA = [
    ("EVENT-KEY-002", "SUMMER2024XYZ",  "Партнёр «Кофейня M»",      0),
    ("EVENT-KEY-003", "PROMO-ABCD-123", "Партнёр «Компания L»",        0),
    ("EVENT-KEY-004", "WELCOME500",     "Партнёр «Корпорация F»",     0),
]


def init_db() -> None:
    if DB_PATH.exists():
        DB_PATH.unlink()
        print(f"[i] Удалена старая БД: {DB_PATH}")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE promo_codes (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            key           TEXT    NOT NULL UNIQUE,
            promo_code    TEXT    NOT NULL,
            partner_name  TEXT    NOT NULL,
            is_used       INTEGER NOT NULL DEFAULT 0,
            created_at    TEXT    NOT NULL DEFAULT (datetime('now'))
        )
    """)

    cursor.executemany(
        "INSERT INTO promo_codes (key, promo_code, partner_name, is_used) "
        "VALUES (?, ?, ?, ?)",
        TEST_DATA
    )

    conn.commit()

    cursor.execute("SELECT key, promo_code, partner_name, is_used FROM promo_codes")
    rows = cursor.fetchall()
    print(f"[+] Создана БД: {DB_PATH}")
    print(f"[+] Загружено записей: {len(rows)}")

    conn.close()


if __name__ == "__main__":
    init_db()
