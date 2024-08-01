import sqlite3

from common import get_timestamp
from config import SQLITE_PATH, TODAY


def get_portfolio_returns(userid, datetime=TODAY):
    timestamp = get_timestamp(datetime)
    with sqlite3.connect(SQLITE_PATH) as conn:
        cur = conn.cursor()
        cur.execute(f'select positions.portfolio_id, stocks.unixtimestamp as date, positions.symbol, positions.shares, stocks.close from stocks JOIN positions on (stocks.unixtimestamp = positions.position_time OR stocks.unixtimestamp=?)AND stocks.symbol = positions.symbol JOIN portfolios ON positions.portfolio_id = portfolios.id JOIN users ON portfolios.user_id = users.id WHERE users.userid = ?', [timestamp, userid])

        positions = cur.fetchall()

        portfolio_ids = list(set([position[0] for position in positions]))
        portfolios = [[] for _ in range(len(portfolio_ids))]
        ref_prices = {position[2]:position[4] for position in positions if position[1]==timestamp}
        print(ref_prices)
        for position in positions:
            if position[1]==timestamp:
                continue
            _return = (ref_prices[position[2]] - position[4]) * position[3]

            status = {
                'symbol': position[2],
                'shares': position[3],
                'return': _return,
                'rateOfReturn': _return / (position[3] * position[4]),
                'value': position[3] * ref_prices[position[2]]
            }
            portfolios[portfolio_ids.index(position[0])].append(status)

        results = []
        for portfolio_idx, portfolio in enumerate(portfolios):
            result = {
                    'portfolio_id': portfolio_ids[portfolio_idx],
                    'stocks':[]
                }
            for status in portfolio:
                result['stocks'].append(status)
            results.append(result)

    return results
