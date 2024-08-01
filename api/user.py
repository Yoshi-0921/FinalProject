from common import AbstractResource


class User(AbstractResource):
    API_PREFIX = '/users/<userid>'

    def get(self, userid):
        cur = self.get_cursor()
        cur.execute('SELECT * FROM users WHERE userid == ?', [userid])
        result = cur.fetchone()
        self.close_cursor()
        return {'users': result}
