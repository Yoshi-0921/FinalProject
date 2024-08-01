from common import AbstractResource

class User(AbstractResource):
    END_POINTS = ['/users', '/users/<userid>']

    def get(self, userid = None):
        cur = self.get_cursor()
        if userid is None:
            cur.execute('SELECT * FROM users')
        else:
            cur.execute('SELECT * FROM users WHERE userid == ?', [userid])
        result = cur.fetchone()
        self.close_cursor()
        return {'users': result}

class UserPositions(AbstractResource):
    END_POINTS = ['/users/<userid>/positions']

    def get(self, userid):
        cur = self.get_cursor()
        cur.execute('SELECT * FROM positions JOIN portfolios ON positions.portfolio_id = portfolios.id JOIN users ON portfolios.user_id = users.id WHERE users.userid = ?', [userid])
        result = cur.fetchall()
        self.close_cursor()
        return {'positions': result}
