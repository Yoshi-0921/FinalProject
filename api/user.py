from common import AbstractResource

class User(AbstractResource):
    END_POINTS = ['/users', '/users/<userid>']

    def get(self, userid):
        cur = self.get_cursor()
        cur.execute('SELECT * FROM users WHERE userid == ?', [userid])
        result = cur.fetchone()
        self.close_cursor()
        return {'users': result}
