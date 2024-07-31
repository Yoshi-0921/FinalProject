from flask import Blueprint, request, Flask
from flask_restful import Resource, Api
from .user import User


app = Flask(__name__)
api = Api(app)

api.add_resource(User, User.USER_API_PREFIX) # /users
