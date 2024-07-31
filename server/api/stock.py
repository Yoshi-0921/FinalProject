import sqlite3

from config import RESOUCE, SQLITE_PATH


class Stock(RESOUCE):
    STOCK_API_PREFIX = '/stocks/<symbol>'
    def get(self, symbol):
        conn = sqlite3.connect(SQLITE_PATH)
        cur = conn.cursor()
        cur.execute('SELECT * FROM stocks WHERE symbol == ?', [symbol])
        result = cur.fetchmany(100)
        cur.close()
        conn.close()
        return {'stocks': result}
