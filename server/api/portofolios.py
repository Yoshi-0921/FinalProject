from common import AbstractResource
from portfolio import get_portfolio_returns


class PortfolioReturns(AbstractResource):
    END_POINTS = ['/returns/<userid>']

    def get(self, userid):
        return get_portfolio_returns(userid)

class Portfolio(AbstractResource):
    END_POINTS = ['/portfolios/<userid>']

    def get(self, userid):
        cur = self.get_cursor()
        cur.execute('SELECT * FROM portfolios JOIN users ON portfolios.user_id = users.id WHERE users.userid == ?', [userid])
        result = cur.fetchall()
        self.close_cursor()
        return {'portfolio': result}
