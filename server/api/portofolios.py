from common import AbstractResource
from portfolio import get_portfolio_returns
from scipy import stats
from functools import wraps
import time
import numpy

class PortfolioReturns(AbstractResource):
    END_POINTS = ['/returns/<userid>']

    def get(self, userid):
        return get_portfolio_returns(userid)

def portfolio_shares(cur, portfolio_id):
    cur.execute('SELECT symbol, shares from positions where portfolio_id = ?;', [portfolio_id])
    result = cur.fetchall()
    return result

class PortfolioShares(AbstractResource):
    END_POINTS = ['/portfolios/<portfolioid>/shares']

    def get(self, portfolioid):
        result = portfolio_shares(self.get_cursor(), portfolioid)
        self.close_cursor()
        return result

class PortfolioGBMParam(AbstractResource):
    # estimate Geometric Brownian Motion parameter for the portfolio from the historical data
    END_POINTS = ['/portfolios/<portfolioid>/gbmparam']

    def get(self, portfolioid):
        cur = self.get_cursor()
        shares = portfolio_shares(cur, portfolioid)
        self.close_cursor()

        query = """
WITH
portfolio_sum AS(
    SELECT
            SUM(CASE
            """
        for share in shares:
            symbol = share[0]
            n = share[1]
            query += f'WHEN stocks.symbol = "{symbol}" THEN stocks.open * {n}\n'
        query += """
        ELSE 0
    END) AS open,
        SUM(CASE
            """
        for share in shares:
            symbol = share[0]
            n = share[1]
            query += f'WHEN stocks.symbol = "{symbol}" THEN stocks.close * {n}\n'
        query += """
    END) AS close
    FROM stocks JOIN positions ON stocks.symbol = positions.symbol WHERE positions.portfolio_id = ? GROUP BY stocks.unixtimestamp ORDER BY unixtimestamp
),
portfolio_var AS(
    SELECT
        (portfolio_sum.close - portfolio_sum.open) / portfolio_sum.open AS var
    FROM portfolio_sum
)
SELECT
    AVG(var),
    AVG(var*var)
FROM portfolio_var
     """
        cur = self.get_cursor()
        cur.execute(query, [portfolioid])
        result = cur.fetchone()
        self.close_cursor()

        muday = result[0]
        sig = (result[1] - result[0]**2)**0.5

        # multiply 250 to make it yearly rate
        # calc stats.lognorm numpy params
        s = sig**2*250
        scale = numpy.exp((muday - 0.5*sig**2)*250)

        return {'s': s, 'scale': scale}


class Portfolio(AbstractResource):
    END_POINTS = ['/portfolios/<userid>']

    def get(self, userid):
        cur = self.get_cursor()
        cur.execute('SELECT * FROM portfolios JOIN users ON portfolios.user_id = users.id WHERE users.userid == ?', [userid])
        result = cur.fetchall()
        self.close_cursor()
        return {'portfolio': result}
