import sqlite3

class Storage:
    def __init__(self, dbpath:str = ".result", dbname:str = "database") -> None:
        self.fullpath = f"{dbpath}/{dbname}.db"

    def init_db(self) -> None:
        pass

    def save_item(self) -> None:
        pass