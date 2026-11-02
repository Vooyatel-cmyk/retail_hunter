import sqlite3
from os import makedirs
from typing import Any

class Storage:
    def __init__(self, dbpath:str = ".result", dbname:str = "database") -> None:
        self.dbpath = dbpath
        self.dbname = dbname or "database"
        self.conn: sqlite3.Connection | None = None

    def __enter__(self) -> "Storage":
        makedirs(self.dbpath, exist_ok=True)
        self.conn = sqlite3.connect(f"{self.dbpath}/{self.dbname}.db")
        return self
    
    def __exit__(self, exc_type, exc, tb) -> None:
        if self.conn is not None:
            if exc_type is not None:
                self.conn.rollback()
            self.conn.close()
            self.conn = None

    def init_db(self) -> None:
        assert self.conn is not None
        self.conn.execute("""CREATE TABLE IF NOT EXISTS products (ID INTEGER PRIMARY KEY, TITLE TEXT UNIQUE, PRICE REAL, STOCK TEXT)""")
        self.conn.commit()


    def save_items(self, products: list[dict[str, Any]]) -> None:
        assert self.conn is not None
        for product in products:
            self.conn.execute(
                "INSERT OR IGNORE INTO products (title, price, stock) VALUES (?, ?, ?)",
                (product["title"], product["raw_price"], product["raw_stock"])
            )
        self.conn.commit()

    def count_items(self) -> int:
        assert self.conn is not None
        return self.conn.execute("SELECT COUNT(*) FROM products").fetchone()[0]