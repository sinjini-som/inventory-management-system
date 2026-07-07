"""
Database layer for the Inventory Management System.
Uses SQLite via the built-in sqlite3 module.
"""

import sqlite3
from contextlib import contextmanager

DB_NAME = "inventory.db"


@contextmanager
def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db():
    """Create tables if they don't exist."""
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                price REAL NOT NULL,
                quantity INTEGER NOT NULL DEFAULT 0,
                low_stock_threshold INTEGER NOT NULL DEFAULT 5
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER NOT NULL,
                quantity_ordered INTEGER NOT NULL,
                order_date TEXT NOT NULL DEFAULT (datetime('now')),
                status TEXT NOT NULL DEFAULT 'PLACED',
                FOREIGN KEY (product_id) REFERENCES products (id)
            )
        """)


def seed_if_empty():
    """Insert a few sample products if the table is empty (nice for first run/demo)."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) as count FROM products")
        if cursor.fetchone()["count"] == 0:
            sample_products = [
                ("Wireless Earbuds", "Electronics", 1999.0, 40, 10),
                ("Running Shoes", "Fashion", 2499.0, 25, 5),
                ("Non Stick Frying Pan", "Home", 899.0, 15, 5),
                ("DSA Textbook", "Books", 599.0, 30, 8),
                ("Yoga Mat", "Sports", 799.0, 3, 5),
            ]
            cursor.executemany(
                "INSERT INTO products (name, category, price, quantity, low_stock_threshold) "
                "VALUES (?, ?, ?, ?, ?)",
                sample_products,
            )


if __name__ == "__main__":
    init_db()
    seed_if_empty()
    print("Database initialized and seeded (if it was empty).")
