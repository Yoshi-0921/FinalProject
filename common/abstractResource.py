import sqlite3

from config import RESOUCE, SQLITE_PATH


class AbstractResource(RESOUCE):
    API_PREFIX = None

    def get_cursor(self):
        self.conn = sqlite3.connect(SQLITE_PATH)
        self.cur = self.conn.cursor()
        return self.cur

    def close_cursor(self):
        self.cur.close()
        self.conn.close()
