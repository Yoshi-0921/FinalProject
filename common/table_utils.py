import sqlite3
from config import SQLITE_PATH
from typing import List


def get_table_columns(table_name: str) -> List[str]:
    with sqlite3.connect(SQLITE_PATH) as conn:
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM {table_name}")
        columns = [description[0] for description in cur.description]

        return columns
