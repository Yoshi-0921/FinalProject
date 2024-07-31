from config import RESOUCE


class User(RESOUCE):
    USER_API_PREFIX = '/users'
    def get(self):
        return {'users': ['Weimeng']}
