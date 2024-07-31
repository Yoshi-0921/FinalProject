import sqlite3

from config import RESOUCE, SQLITE_PATH


class User(RESOUCE):
    USER_API_PREFIX = '/users/<userid>'
    def get(self, userid):
        conn = sqlite3.connect(SQLITE_PATH)
        cur = conn.cursor()
        cur.execute('SELECT * FROM users WHERE userid == ?', [userid])
        result = cur.fetchone()
        cur.close()
        conn.close()
        return {'users': result}
