# TODO: change to environment variables
debug = True

if debug:
    from flask_restx import Resource, Api
else:
    from flask_restful import Resource, Api 

from main import app

api = Api(app)

from .user import *
api.add_resource(User, User.USER_API_PREFIX) # /users



