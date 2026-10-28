import sqlite3
from typing import Any

class Storage:
    def __init__(self, dbpath:str = ".result", dbname:str = "database") -> None:
        self.conn = sqlite3.connect(f"{dbpath}/{dbname}.db")

    def init_db(self) -> None:
        self.conn.execute("""CREATE TABLE IF NOT EXISTS PRODUCTS (ID INTEGER PRIMARY KEY, TITLE TEXT UNIQUE, PRICE REAL, STOCK TEXT)""")
        self.conn.commit()


    def save_items(self, products: list[dict[str, Any]]) -> None:
        for product in products:
            self.conn.execute(
                "INSERT OR IGNORE INTO products (title, price, stock) VALUES (?, ?, ?)",
                (product["title"], product["raw_price"], product["raw_stock"])
            )
        self.conn.commit()

    def count_items(self) -> None:
        pass

    def close_db(self) -> None:
        self.conn.close()