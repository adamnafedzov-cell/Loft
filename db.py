import aiosqlite
import os
from datetime import datetime

DB_PATH = os.getenv("DB_PATH", "data/reviews.db")

CREATE_SQL = """
CREATE TABLE IF NOT EXISTS reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    table_id TEXT,
    category TEXT,
    review_text TEXT,
    created_at TEXT
);
"""

async def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(CREATE_SQL)
        await db.commit()

async def insert_review(table_id: str, category: str, review_text: str, created_at: str = None):
    created_at = created_at or datetime.utcnow().isoformat()
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO reviews (table_id, category, review_text, created_at) VALUES (?, ?, ?, ?)",
            (table_id, category, review_text, created_at)
        )
        await db.commit()

async def fetch_all_reviews():
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("SELECT id, table_id, category, review_text, created_at FROM reviews ORDER BY id DESC")
        rows = await cursor.fetchall()
        return rows

async def delete_review(review_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("DELETE FROM reviews WHERE id = ?", (review_id,))
        await db.commit()
