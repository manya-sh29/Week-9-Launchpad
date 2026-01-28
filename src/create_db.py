import sqlite3
from pathlib import Path

DB_PATH = Path("sales.db")

def create_sales_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT NOT NULL,
            quarter TEXT NOT NULL,
            year INTEGER NOT NULL,
            revenue REAL NOT NULL
        );
    """)

    cursor.executemany(
        """
        INSERT INTO sales (company, quarter, year, revenue)
        VALUES (?, ?, ?, ?);
        """,
        [
            ("Y", "Q1", 2026, 120000.50),
            ("Y", "Q1", 2026, 83000.75),
            ("X", "Q1", 2026, 95000.00),
            ("X", "Q2", 2026, 102000.00),
            ("Y", "Q2", 2026, 142000.00),
            ("Z", "Q1", 2026, 77000.25),
            ("Z", "Q2", 2026, 88000.50),
            ("X", "Q3", 2026, 99000.00),
            ("Y", "Q3", 2026, 130000.75),
            ("Z", "Q3", 2026, 92000.00),
        ]
    )

    conn.commit()

    conn.close()


if __name__ == "__main__":
    if DB_PATH.exists():
        print("sales.db already exists")
    else:
        create_sales_db()
        print("sales.db created successfully with 10 entries")
