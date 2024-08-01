import sqlite3
from typing import List
from config import RESOUCE, SQLITE_PATH


class AbstractResource(RESOUCE):
    END_POINTS: List[str] = None

    def get_cursor(self):
        self.conn = sqlite3.connect(SQLITE_PATH)
        self.cur = self.conn.cursor()
        return self.cur

    def close_cursor(self):
        self.cur.close()
        self.conn.close()
