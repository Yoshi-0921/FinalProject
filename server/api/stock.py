from common import AbstractResource


class Stock(AbstractResource):
    API_PREFIX = '/stocks/<symbol>'

    def get(self, symbol):
        cur = self.get_cursor()
        cur.execute('SELECT * FROM stocks WHERE symbol == ?', [symbol])
        result = cur.fetchmany(100)
        self.close_cursor()
        return {'stocks': result}
