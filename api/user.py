from flask_restful import api
from user import User


api.add_resource(User, User.USER_API_PREFIX) # /users


