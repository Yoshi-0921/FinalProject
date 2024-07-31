from . import Resource


class User(Resource):
    USER_API_PREFIX = '/users'
    def get(self):
        return {'users': ['Weimeng']}
