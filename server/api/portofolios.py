from common import AbstractResource
from portfolio import get_portfolio_returns


class Portfolio(AbstractResource):
    END_POINTS = ['/portfolios/<username>']

    def get(self, username):
        return get_portfolio_returns(username)
