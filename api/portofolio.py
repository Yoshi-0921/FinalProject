from common import AbstractResource

class Portfolio(AbstractResource):
    END_POINTS = ['/portfolios/<username>']

    def get(self, username):
        raise NotImplementedError
