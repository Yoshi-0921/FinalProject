from common import AbstractResource
from flask import request
from . import api

class Stock(AbstractResource):
    END_POINTS = ['/stocks/<symbol>']

    @api.doc(params={
        'from': {
            'description': 'starting unix timestamp',
            'type': 'int'
        },
        'to': {
            'description': 'ending unix timestamp',
            'type': 'int'
        },
        'intervalday': {
            'description': 'interval (day)',
            'type': 'int',
            'default': 1
        },
        'limit': {
            'description': 'max number to fetch results',
            'type': 'int',
            'default': 100
        }})
    def get(self, symbol):
        from_t = request.args.get('from', default=None, type=int)
        to_t = request.args.get('to', default=None, type=int)
        intervalday = request.args.get('intervalday', default=1, type=int)
        limit = request.args.get('limit', default=100, type=int)

        variable_clause = []
        if from_t is not None:
            variable_clause.append(f'unixtimestamp >= {from_t}')
        if to_t is not None:
            variable_clause.append(f'unixtimestamp <= {to_t}')
        variable_clause_str = ' AND '.join(variable_clause)
        if variable_clause_str != '':
            variable_clause_str = ' AND ' + variable_clause_str
        print(variable_clause_str)

        cur = self.get_cursor()
        cur.execute('SELECT * FROM stocks WHERE id%? = 0 AND symbol = ?' + variable_clause_str + ' LIMIT ?', [intervalday, symbol, limit])
        result = cur.fetchall()
        self.close_cursor()
        return {'stocks': result}
